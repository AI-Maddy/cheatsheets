================================
Linux Network Drivers Guide
================================

:Author: Linux Kernel Documentation
:Date: January 2026
:Version: 1.0
:Kernel: 5.x, 6.x

.. contents:: Table of Contents
   :depth: 3

TL;DR - Quick Reference
=======================

Basic Network Driver
--------------------

.. code-block:: c

   #include <linux/netdevice.h>
   #include <linux/etherdevice.h>
   
   static netdev_tx_t mynet_xmit(struct sk_buff *skb, struct net_device *dev) {
       struct mynet_priv *priv = netdev_priv(dev);
       
       /* Transmit packet */
       mynet_hw_tx(priv, skb->data, skb->len);
       
       /* Update stats */
       dev->stats.tx_packets++;
       dev->stats.tx_bytes += skb->len;
       
       dev_kfree_skb(skb);
       return NETDEV_TX_OK;
   }
   
   static int mynet_open(struct net_device *dev) {
       netif_start_queue(dev);
       return 0;
   }
   
   static int mynet_stop(struct net_device *dev) {
       netif_stop_queue(dev);
       return 0;
   }
   
   static const struct net_device_ops mynet_ops = {
       .ndo_open = mynet_open,
       .ndo_stop = mynet_stop,
       .ndo_start_xmit = mynet_xmit,
   };
   
   /* Setup and register */
   struct net_device *dev;
   dev = alloc_etherdev(sizeof(struct mynet_priv));
   dev->netdev_ops = &mynet_ops;
   register_netdev(dev);

RX Packet Handling
------------------

.. code-block:: c

   static irqreturn_t mynet_irq(int irq, void *data) {
       struct net_device *dev = data;
       struct mynet_priv *priv = netdev_priv(dev);
       struct sk_buff *skb;
       
       /* Allocate sk_buff */
       skb = netdev_alloc_skb(dev, pkt_len + NET_IP_ALIGN);
       skb_reserve(skb, NET_IP_ALIGN);
       
       /* Copy data from hardware */
       mynet_hw_rx(priv, skb_put(skb, pkt_len), pkt_len);
       
       /* Set protocol */
       skb->protocol = eth_type_trans(skb, dev);
       
       /* Pass to network stack */
       netif_rx(skb);
       
       /* Update stats */
       dev->stats.rx_packets++;
       dev->stats.rx_bytes += pkt_len;
       
       return IRQ_HANDLED;
   }

Network Device Basics
======================

net_device Structure
--------------------

.. code-block:: c

   struct net_device {
       char name[IFNAMSIZ];
       unsigned char *dev_addr;  // MAC address
       unsigned int mtu;
       unsigned int flags;
       const struct net_device_ops *netdev_ops;
       const struct ethtool_ops *ethtool_ops;
       struct net_device_stats stats;
       // ... many more fields
   };

Allocating Network Device
--------------------------

.. code-block:: c

   /* Ethernet device */
   struct net_device *dev;
   struct mynet_priv *priv;
   
   dev = alloc_etherdev(sizeof(struct mynet_priv));
   if (!dev)
       return -ENOMEM;
   
   priv = netdev_priv(dev);
   priv->dev = dev;
   
   /* Generic network device */
   dev = alloc_netdev(sizeof(struct mynet_priv), "eth%d",
                       NET_NAME_UNKNOWN, ether_setup);
   
   /* Later: free */
   free_netdev(dev);

Network Device Operations
==========================

net_device_ops
--------------

.. code-block:: c

   static const struct net_device_ops mynet_ops = {
       .ndo_open = mynet_open,
       .ndo_stop = mynet_stop,
       .ndo_start_xmit = mynet_start_xmit,
       .ndo_set_rx_mode = mynet_set_rx_mode,
       .ndo_set_mac_address = mynet_set_mac_address,
       .ndo_validate_addr = eth_validate_addr,
       .ndo_do_ioctl = mynet_ioctl,
       .ndo_change_mtu = eth_change_mtu,
       .ndo_tx_timeout = mynet_tx_timeout,
       .ndo_get_stats64 = mynet_get_stats64,
   };

Open/Close
----------

.. code-block:: c

   static int mynet_open(struct net_device *dev) {
       struct mynet_priv *priv = netdev_priv(dev);
       int ret;
       
       /* Request IRQ */
       ret = request_irq(dev->irq, mynet_irq, IRQF_SHARED, dev->name, dev);
       if (ret)
           return ret;
       
       /* Allocate DMA buffers */
       ret = mynet_alloc_buffers(priv);
       if (ret) {
           free_irq(dev->irq, dev);
           return ret;
       }
       
       /* Initialize hardware */
       mynet_hw_init(priv);
       
       /* Enable interrupts */
       mynet_enable_irq(priv);
       
       /* Start TX queue */
       netif_start_queue(dev);
       
       return 0;
   }
   
   static int mynet_stop(struct net_device *dev) {
       struct mynet_priv *priv = netdev_priv(dev);
       
       /* Stop TX queue */
       netif_stop_queue(dev);
       
       /* Disable interrupts */
       mynet_disable_irq(priv);
       
       /* Stop hardware */
       mynet_hw_stop(priv);
       
       /* Free IRQ */
       free_irq(dev->irq, dev);
       
       /* Free buffers */
       mynet_free_buffers(priv);
       
       return 0;
   }

TX Path
=======

Transmit Function
-----------------

.. code-block:: c

   static netdev_tx_t mynet_start_xmit(struct sk_buff *skb,
                                        struct net_device *dev) {
       struct mynet_priv *priv = netdev_priv(dev);
       unsigned long flags;
       
       spin_lock_irqsave(&priv->lock, flags);
       
       /* Check if TX queue has space */
       if (mynet_tx_full(priv)) {
           netif_stop_queue(dev);
           spin_unlock_irqrestore(&priv->lock, flags);
           return NETDEV_TX_BUSY;
       }
       
       /* Save timestamp for TX timeout */
       netdev_trans_update(dev);
       
       /* DMA mapping if needed */
       dma_addr_t dma_addr;
       dma_addr = dma_map_single(&priv->pdev->dev, skb->data, skb->len,
                                  DMA_TO_DEVICE);
       if (dma_mapping_error(&priv->pdev->dev, dma_addr)) {
           dev->stats.tx_errors++;
           dev_kfree_skb(skb);
           spin_unlock_irqrestore(&priv->lock, flags);
           return NETDEV_TX_OK;
       }
       
       /* Store skb for TX complete */
       priv->tx_skb[priv->tx_head] = skb;
       priv->tx_dma[priv->tx_head] = dma_addr;
       
       /* Write to TX descriptor */
       mynet_hw_tx_desc(priv, dma_addr, skb->len);
       
       priv->tx_head = (priv->tx_head + 1) % TX_RING_SIZE;
       
       /* Update stats */
       dev->stats.tx_packets++;
       dev->stats.tx_bytes += skb->len;
       
       spin_unlock_irqrestore(&priv->lock, flags);
       
       return NETDEV_TX_OK;
   }

TX Complete (in IRQ handler)
-----------------------------

.. code-block:: c

   static void mynet_tx_complete(struct mynet_priv *priv) {
       struct net_device *dev = priv->dev;
       
       while (priv->tx_tail != priv->tx_head) {
           struct sk_buff *skb = priv->tx_skb[priv->tx_tail];
           dma_addr_t dma_addr = priv->tx_dma[priv->tx_tail];
           
           /* Check if TX complete */
           if (!mynet_hw_tx_done(priv, priv->tx_tail))
               break;
           
           /* Unmap DMA */
           dma_unmap_single(&priv->pdev->dev, dma_addr, skb->len,
                             DMA_TO_DEVICE);
           
           /* Free sk_buff */
           dev_consume_skb_irq(skb);
           
           priv->tx_tail = (priv->tx_tail + 1) % TX_RING_SIZE;
       }
       
       /* Wake TX queue if it was stopped */
       if (netif_queue_stopped(dev) && !mynet_tx_full(priv))
           netif_wake_queue(dev);
   }

RX Path
=======

Receive Processing
------------------

.. code-block:: c

   static int mynet_rx_poll(struct napi_struct *napi, int budget) {
       struct mynet_priv *priv = container_of(napi, struct mynet_priv, napi);
       struct net_device *dev = priv->dev;
       int work_done = 0;
       
       while (work_done < budget) {
           struct sk_buff *skb;
           u16 pkt_len;
           
           /* Check if RX data available */
           if (!mynet_hw_rx_ready(priv))
               break;
           
           pkt_len = mynet_hw_rx_len(priv);
           
           /* Allocate sk_buff */
           skb = netdev_alloc_skb(dev, pkt_len + NET_IP_ALIGN);
           if (!skb) {
               dev->stats.rx_dropped++;
               mynet_hw_rx_drop(priv);
               break;
           }
           
           /* Reserve for IP header alignment */
           skb_reserve(skb, NET_IP_ALIGN);
           
           /* Copy data from hardware */
           mynet_hw_rx_data(priv, skb_put(skb, pkt_len), pkt_len);
           
           /* Set protocol */
           skb->protocol = eth_type_trans(skb, dev);
           skb->ip_summed = CHECKSUM_NONE;
           
           /* Pass to network stack */
           napi_gro_receive(napi, skb);
           
           /* Update stats */
           dev->stats.rx_packets++;
           dev->stats.rx_bytes += pkt_len;
           
           work_done++;
       }
       
       /* If not all budget used, complete NAPI */
       if (work_done < budget) {
           napi_complete_done(napi, work_done);
           mynet_enable_rx_irq(priv);
       }
       
       return work_done;
   }

NAPI Setup
----------

.. code-block:: c

   static int mynet_probe(struct platform_device *pdev) {
       /* ... */
       
       /* Initialize NAPI */
       netif_napi_add(dev, &priv->napi, mynet_rx_poll, 64);
       
       /* ... */
   }
   
   static irqreturn_t mynet_irq(int irq, void *data) {
       struct net_device *dev = data;
       struct mynet_priv *priv = netdev_priv(dev);
       u32 status;
       
       status = mynet_read_irq_status(priv);
       
       if (status & RX_IRQ) {
           /* Disable RX IRQ and schedule NAPI */
           mynet_disable_rx_irq(priv);
           napi_schedule(&priv->napi);
       }
       
       if (status & TX_IRQ) {
           mynet_tx_complete(priv);
       }
       
       return IRQ_HANDLED;
   }

Complete Driver Example
========================

Platform Ethernet Driver
------------------------

.. code-block:: c

   #include <linux/module.h>
   #include <linux/platform_device.h>
   #include <linux/netdevice.h>
   #include <linux/etherdevice.h>
   #include <linux/interrupt.h>
   #include <linux/io.h>
   #include <linux/dma-mapping.h>
   
   #define TX_RING_SIZE 16
   #define RX_RING_SIZE 16
   
   struct mynet_priv {
       struct net_device *dev;
       struct platform_device *pdev;
       void __iomem *regs;
       int irq;
       
       struct napi_struct napi;
       spinlock_t lock;
       
       /* TX ring */
       struct sk_buff *tx_skb[TX_RING_SIZE];
       dma_addr_t tx_dma[TX_RING_SIZE];
       unsigned int tx_head;
       unsigned int tx_tail;
       
       /* RX ring */
       struct sk_buff *rx_skb[RX_RING_SIZE];
       dma_addr_t rx_dma[RX_RING_SIZE];
       unsigned int rx_head;
   };
   
   static netdev_tx_t mynet_start_xmit(struct sk_buff *skb,
                                        struct net_device *dev) {
       /* See TX Path section above */
       return NETDEV_TX_OK;
   }
   
   static int mynet_open(struct net_device *dev) {
       struct mynet_priv *priv = netdev_priv(dev);
       int ret;
       
       ret = request_irq(priv->irq, mynet_irq, 0, dev->name, dev);
       if (ret)
           return ret;
       
       napi_enable(&priv->napi);
       netif_start_queue(dev);
       
       return 0;
   }
   
   static int mynet_stop(struct net_device *dev) {
       struct mynet_priv *priv = netdev_priv(dev);
       
       netif_stop_queue(dev);
       napi_disable(&priv->napi);
       free_irq(priv->irq, dev);
       
       return 0;
   }
   
   static void mynet_set_rx_mode(struct net_device *dev) {
       /* Handle promiscuous/multicast modes */
   }
   
   static int mynet_set_mac_address(struct net_device *dev, void *addr) {
       struct sockaddr *sa = addr;
       
       if (!is_valid_ether_addr(sa->sa_data))
           return -EADDRNOTAVAIL;
       
       eth_hw_addr_set(dev, sa->sa_data);
       
       return 0;
   }
   
   static const struct net_device_ops mynet_ops = {
       .ndo_open = mynet_open,
       .ndo_stop = mynet_stop,
       .ndo_start_xmit = mynet_start_xmit,
       .ndo_set_rx_mode = mynet_set_rx_mode,
       .ndo_set_mac_address = mynet_set_mac_address,
       .ndo_validate_addr = eth_validate_addr,
   };
   
   static int mynet_probe(struct platform_device *pdev) {
       struct net_device *dev;
       struct mynet_priv *priv;
       struct resource *res;
       int ret;
       
       /* Allocate network device */
       dev = alloc_etherdev(sizeof(struct mynet_priv));
       if (!dev)
           return -ENOMEM;
       
       SET_NETDEV_DEV(dev, &pdev->dev);
       platform_set_drvdata(pdev, dev);
       
       priv = netdev_priv(dev);
       priv->dev = dev;
       priv->pdev = pdev;
       spin_lock_init(&priv->lock);
       
       /* Map registers */
       res = platform_get_resource(pdev, IORESOURCE_MEM, 0);
       priv->regs = devm_ioremap_resource(&pdev->dev, res);
       if (IS_ERR(priv->regs)) {
           ret = PTR_ERR(priv->regs);
           goto err_free_dev;
       }
       
       /* Get IRQ */
       priv->irq = platform_get_irq(pdev, 0);
       if (priv->irq < 0) {
           ret = priv->irq;
           goto err_free_dev;
       }
       
       /* Setup DMA */
       ret = dma_set_mask_and_coherent(&pdev->dev, DMA_BIT_MASK(32));
       if (ret)
           goto err_free_dev;
       
       /* Setup network device */
       dev->netdev_ops = &mynet_ops;
       dev->irq = priv->irq;
       
       /* Set MAC address */
       eth_hw_addr_random(dev);
       
       /* Initialize NAPI */
       netif_napi_add(dev, &priv->napi, mynet_rx_poll, 64);
       
       /* Register network device */
       ret = register_netdev(dev);
       if (ret) {
           netdev_err(dev, "Failed to register network device\n");
           goto err_napi;
       }
       
       netdev_info(dev, "Network device registered\n");
       return 0;
       
   err_napi:
       netif_napi_del(&priv->napi);
   err_free_dev:
       free_netdev(dev);
       return ret;
   }
   
   static int mynet_remove(struct platform_device *pdev) {
       struct net_device *dev = platform_get_drvdata(pdev);
       struct mynet_priv *priv = netdev_priv(dev);
       
       unregister_netdev(dev);
       netif_napi_del(&priv->napi);
       free_netdev(dev);
       
       return 0;
   }
   
   static const struct of_device_id mynet_of_match[] = {
       { .compatible = "vendor,ethernet", },
       { }
   };
   MODULE_DEVICE_TABLE(of, mynet_of_match);
   
   static struct platform_driver mynet_driver = {
       .driver = {
           .name = "mynet",
           .of_match_table = mynet_of_match,
       },
       .probe = mynet_probe,
       .remove = mynet_remove,
   };
   
   module_platform_driver(mynet_driver);
   
   MODULE_LICENSE("GPL");
   MODULE_DESCRIPTION("Network Driver");

Ethtool Support
===============

.. code-block:: c

   static void mynet_get_drvinfo(struct net_device *dev,
                                  struct ethtool_drvinfo *info) {
       strlcpy(info->driver, "mynet", sizeof(info->driver));
       strlcpy(info->version, "1.0", sizeof(info->version));
   }
   
   static int mynet_get_link_ksettings(struct net_device *dev,
                                        struct ethtool_link_ksettings *cmd) {
       cmd->base.speed = SPEED_100;
       cmd->base.duplex = DUPLEX_FULL;
       cmd->base.port = PORT_MII;
       cmd->base.autoneg = AUTONEG_DISABLE;
       
       return 0;
   }
   
   static const struct ethtool_ops mynet_ethtool_ops = {
       .get_drvinfo = mynet_get_drvinfo,
       .get_link = ethtool_op_get_link,
       .get_link_ksettings = mynet_get_link_ksettings,
   };
   
   /* In probe */
   dev->ethtool_ops = &mynet_ethtool_ops;

Best Practices
==============

1. **Use NAPI** for RX processing
2. **Implement proper locking** (spinlock for registers)
3. **Handle DMA mapping** correctly
4. **Free skbs** in appropriate context
5. **Update statistics** accurately
6. **Support ethtool** operations
7. **Use netdev_* logging** functions
8. **Implement TX timeout** handler
9. **Handle carrier state** properly
10. **Test with netperf/iperf**

Common Pitfalls
===============

1. **Not using NAPI** (poor performance)
2. **Calling netif_rx()** from hard IRQ
3. **DMA mapping errors**
4. **Memory leaks** with sk_buffs
5. **Wrong lock context**
6. **Not handling TX queue full**

Debugging
=========

.. code-block:: bash

   # Check interface
   ip link show eth0
   ifconfig eth0
   
   # View statistics
   ip -s link show eth0
   ethtool -S eth0
   
   # Test performance
   iperf3 -s  # Server
   iperf3 -c <ip>  # Client
   
   # Packet capture
   tcpdump -i eth0
   
   # Enable driver debug
   ethtool -s eth0 msglvl 0xffff

See Also
========

- Linux_Platform_Drivers.rst
- Linux_Driver_IRQ_Handling.rst
- Linux_DMA.rst

References
==========

- Documentation/networking/netdevices.rst
- include/linux/netdevice.h
- include/linux/etherdevice.h
