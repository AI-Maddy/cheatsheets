=============================================
Embedded State Machines
=============================================

:Author: Embedded Systems Design Patterns Documentation
:Date: January 2026
:Version: 1.0
:Focus: State machine design patterns and implementations

.. contents:: Table of Contents
   :depth: 3

TL;DR - Quick Reference
=======================

State Machine Concepts
-----------------------

.. code-block:: text

   State Machine Types:
   
   1. Flat State Machine (FSM)
      - Simple states and transitions
      - Switch/case or table-driven
   
   2. Hierarchical State Machine (HSM)
      - Nested states (substates)
      - State inheritance
   
   3. UML Statecharts
      - Orthogonal regions
      - Entry/exit actions
      - Internal transitions
   
   4. Event-Driven
      - Events trigger transitions
      - Decoupled architecture
   
   Implementation Approaches:
   - Switch/case (simple)
   - Function pointers (flexible)
   - Table-driven (compact)
   - Object-oriented (scalable)

Simple State Machine
====================

Switch-Based FSM
----------------

.. code-block:: c

   // States
   typedef enum {
       STATE_IDLE,
       STATE_RUNNING,
       STATE_PAUSED,
       STATE_ERROR
   } State;
   
   // Events
   typedef enum {
       EVENT_START,
       EVENT_STOP,
       EVENT_PAUSE,
       EVENT_RESUME,
       EVENT_ERROR
   } Event;
   
   // State machine
   typedef struct {
       State current_state;
   } StateMachine;
   
   void StateMachine_Init(StateMachine *self) {
       self->current_state = STATE_IDLE;
   }
   
   void StateMachine_ProcessEvent(StateMachine *self, Event event) {
       switch (self->current_state) {
       case STATE_IDLE:
           if (event == EVENT_START) {
               // Exit actions
               cleanup_idle();
               
               // Transition
               self->current_state = STATE_RUNNING;
               
               // Entry actions
               initialize_running();
           }
           break;
           
       case STATE_RUNNING:
           if (event == EVENT_STOP) {
               self->current_state = STATE_IDLE;
           } else if (event == EVENT_PAUSE) {
               self->current_state = STATE_PAUSED;
           } else if (event == EVENT_ERROR) {
               self->current_state = STATE_ERROR;
               handle_error();
           }
           break;
           
       case STATE_PAUSED:
           if (event == EVENT_RESUME) {
               self->current_state = STATE_RUNNING;
           } else if (event == EVENT_STOP) {
               self->current_state = STATE_IDLE;
           }
           break;
           
       case STATE_ERROR:
           if (event == EVENT_STOP) {
               clear_error();
               self->current_state = STATE_IDLE;
           }
           break;
       }
   }

Function Pointer FSM
--------------------

.. code-block:: c

   // Forward declaration
   typedef struct StateMachine StateMachine;
   
   // State handler function
   typedef void (*StateHandler_fn)(StateMachine *self, Event event);
   
   struct StateMachine {
       StateHandler_fn current_state;
   };
   
   // State handler functions
   void state_idle(StateMachine *self, Event event);
   void state_running(StateMachine *self, Event event);
   void state_paused(StateMachine *self, Event event);
   void state_error(StateMachine *self, Event event);
   
   void state_idle(StateMachine *self, Event event) {
       switch (event) {
       case EVENT_START:
           self->current_state = state_running;
           initialize_running();
           break;
       default:
           // Ignore other events
           break;
       }
   }
   
   void state_running(StateMachine *self, Event event) {
       switch (event) {
       case EVENT_STOP:
           self->current_state = state_idle;
           cleanup_running();
           break;
       case EVENT_PAUSE:
           self->current_state = state_paused;
           save_state();
           break;
       case EVENT_ERROR:
           self->current_state = state_error;
           handle_error();
           break;
       default:
           break;
       }
   }
   
   void state_paused(StateMachine *self, Event event) {
       switch (event) {
       case EVENT_RESUME:
           self->current_state = state_running;
           restore_state();
           break;
       case EVENT_STOP:
           self->current_state = state_idle;
           cleanup_running();
           break;
       default:
           break;
       }
   }
   
   void StateMachine_Init(StateMachine *self) {
       self->current_state = state_idle;
   }
   
   void StateMachine_ProcessEvent(StateMachine *self, Event event) {
       self->current_state(self, event);
   }

Table-Driven FSM
================

Transition Table
----------------

.. code-block:: c

   // Transition table entry
   typedef struct {
       State current_state;
       Event event;
       State next_state;
       void (*action)(void);
   } Transition;
   
   // Actions
   void action_start_running(void) {
       initialize_running();
   }
   
   void action_pause(void) {
       save_state();
   }
   
   void action_resume(void) {
       restore_state();
   }
   
   void action_stop(void) {
       cleanup_running();
   }
   
   void action_error(void) {
       handle_error();
   }
   
   // Transition table
   static const Transition transition_table[] = {
       // Current State   Event           Next State       Action
       {STATE_IDLE,       EVENT_START,    STATE_RUNNING,   action_start_running},
       {STATE_RUNNING,    EVENT_STOP,     STATE_IDLE,      action_stop},
       {STATE_RUNNING,    EVENT_PAUSE,    STATE_PAUSED,    action_pause},
       {STATE_RUNNING,    EVENT_ERROR,    STATE_ERROR,     action_error},
       {STATE_PAUSED,     EVENT_RESUME,   STATE_RUNNING,   action_resume},
       {STATE_PAUSED,     EVENT_STOP,     STATE_IDLE,      action_stop},
       {STATE_ERROR,      EVENT_STOP,     STATE_IDLE,      action_stop},
   };
   
   #define NUM_TRANSITIONS (sizeof(transition_table) / sizeof(Transition))
   
   void StateMachine_ProcessEvent(StateMachine *self, Event event) {
       for (size_t i = 0; i < NUM_TRANSITIONS; i++) {
           if (transition_table[i].current_state == self->current_state &&
               transition_table[i].event == event) {
               
               // Execute action
               if (transition_table[i].action) {
                   transition_table[i].action();
               }
               
               // Transition to next state
               self->current_state = transition_table[i].next_state;
               return;
           }
       }
       
       // Event not handled
   }

Hierarchical State Machine (HSM)
=================================

Intent
------

Organize states in a hierarchy where substates inherit behavior from parent states.

Structure
---------

.. code-block:: c

   // State structure
   typedef struct State State;
   typedef State (*StateHandler_fn)(State *self, Event event);
   
   struct State {
       StateHandler_fn handler;
       State *parent;        // Parent state (NULL for top)
       const char *name;     // For debugging
   };
   
   // Special return values
   #define STATE_HANDLED()     ((State){NULL, NULL, "HANDLED"})
   #define STATE_IGNORED()     ((State){NULL, (State*)1, "IGNORED"})
   #define STATE_TRANSITION(s) ((State){(s)->handler, (s)->parent, (s)->name})
   
   #define IS_HANDLED(s)       ((s).parent == NULL && (s).handler == NULL)
   #define IS_IGNORED(s)       ((s).parent == (State*)1)
   #define IS_TRANSITION(s)    ((s).handler != NULL)
   
   // Machine structure
   typedef struct {
       State *current;
       State *source;  // For transitions
   } HSM;
   
   // Special events
   #define EVENT_ENTRY   0xFF
   #define EVENT_EXIT    0xFE
   #define EVENT_INIT    0xFD

Example: Motor Controller HSM
------------------------------

.. code-block:: c

   // Forward declarations
   State motor_top(State *self, Event event);
   State motor_stopped(State *self, Event event);
   State motor_running(State *self, Event event);
   State motor_forward(State *self, Event event);
   State motor_reverse(State *self, Event event);
   State motor_error(State *self, Event event);
   
   // State definitions
   State state_motor_top      = {motor_top,      NULL,                "TOP"};
   State state_motor_stopped  = {motor_stopped,  &state_motor_top,    "STOPPED"};
   State state_motor_running  = {motor_running,  &state_motor_top,    "RUNNING"};
   State state_motor_forward  = {motor_forward,  &state_motor_running, "FORWARD"};
   State state_motor_reverse  = {motor_reverse,  &state_motor_running, "REVERSE"};
   State state_motor_error    = {motor_error,    &state_motor_top,    "ERROR"};
   
   // Top state (handles common events)
   State motor_top(State *self, Event event) {
       switch (event) {
       case EVENT_ERROR:
           return STATE_TRANSITION(&state_motor_error);
           
       case EVENT_STOP:
           return STATE_TRANSITION(&state_motor_stopped);
       }
       
       return STATE_IGNORED();
   }
   
   // Stopped state
   State motor_stopped(State *self, Event event) {
       switch (event) {
       case EVENT_ENTRY:
           disable_motor();
           return STATE_HANDLED();
           
       case EVENT_EXIT:
           enable_motor();
           return STATE_HANDLED();
           
       case EVENT_START:
           return STATE_TRANSITION(&state_motor_forward);
       }
       
       return STATE_IGNORED();  // Delegate to parent
   }
   
   // Running state (parent of forward/reverse)
   State motor_running(State *self, Event event) {
       switch (event) {
       case EVENT_ENTRY:
           start_pwm();
           return STATE_HANDLED();
           
       case EVENT_EXIT:
           stop_pwm();
           return STATE_HANDLED();
           
       case EVENT_INIT:
           // Initial substate
           return STATE_TRANSITION(&state_motor_forward);
       }
       
       return STATE_IGNORED();
   }
   
   // Forward state
   State motor_forward(State *self, Event event) {
       switch (event) {
       case EVENT_ENTRY:
           set_direction_forward();
           return STATE_HANDLED();
           
       case EVENT_REVERSE:
           return STATE_TRANSITION(&state_motor_reverse);
       }
       
       return STATE_IGNORED();
   }
   
   // Reverse state
   State motor_reverse(State *self, Event event) {
       switch (event) {
       case EVENT_ENTRY:
           set_direction_reverse();
           return STATE_HANDLED();
           
       case EVENT_FORWARD:
           return STATE_TRANSITION(&state_motor_forward);
       }
       
       return STATE_IGNORED();
   }

HSM Dispatch
------------

.. code-block:: c

   void HSM_Init(HSM *self, State *initial) {
       self->current = initial;
       
       State result = initial->handler(initial, EVENT_ENTRY);
       
       // Process INIT event if needed
       if (IS_TRANSITION(result)) {
           State *target = &result;
           target->handler(target, EVENT_ENTRY);
           self->current = target;
       }
   }
   
   void HSM_Dispatch(HSM *self, Event event) {
       State *s = self->current;
       State result;
       
       // Try current state and parents
       while (s) {
           result = s->handler(s, event);
           
           if (IS_HANDLED(result)) {
               return;  // Event handled
           } else if (IS_TRANSITION(result)) {
               // Transition
               State *target = &result;
               
               // Find common parent
               State *lca = find_lca(self->current, target);
               
               // Exit from current to LCA
               State *temp = self->current;
               while (temp != lca) {
                   temp->handler(temp, EVENT_EXIT);
                   temp = temp->parent;
               }
               
               // Enter from LCA to target
               enter_state_path(lca, target);
               
               self->current = target;
               return;
           }
           
           // Try parent
           s = s->parent;
       }
   }
   
   // Helper to find lowest common ancestor
   State *find_lca(State *s1, State *s2) {
       // Build path to root for s1
       State *path[MAX_DEPTH];
       int depth = 0;
       
       State *temp = s1;
       while (temp) {
           path[depth++] = temp;
           temp = temp->parent;
       }
       
       // Walk s2's path and find first match
       temp = s2;
       while (temp) {
           for (int i = 0; i < depth; i++) {
               if (path[i] == temp) {
                   return temp;
               }
           }
           temp = temp->parent;
       }
       
       return NULL;
   }

UML Statecharts
===============

Extended Features
-----------------

.. code-block:: c

   // State with entry, exit, and do activities
   typedef struct {
       State base;
       void (*on_entry)(void);
       void (*on_exit)(void);
       void (*do_activity)(void);
       uint32_t entry_time;
   } ExtendedState;
   
   // Guard conditions
   typedef bool (*Guard_fn)(void);
   
   typedef struct {
       State current_state;
       Event event;
       Guard_fn guard;
       State next_state;
       void (*action)(void);
   } GuardedTransition;
   
   // Example with guards
   bool temperature_high(void) {
       return read_temperature() > 50.0f;
   }
   
   bool battery_low(void) {
       return read_battery() < 10.0f;
   }
   
   GuardedTransition guarded_table[] = {
       {STATE_RUNNING, EVENT_CHECK, temperature_high, STATE_OVERHEAT, activate_cooling},
       {STATE_RUNNING, EVENT_CHECK, battery_low,      STATE_LOWPOWER, reduce_power},
   };
   
   void process_guarded_event(StateMachine *self, Event event) {
       for (size_t i = 0; i < NUM_GUARDED; i++) {
           if (guarded_table[i].current_state == self->current_state &&
               guarded_table[i].event == event) {
               
               // Check guard
               if (!guarded_table[i].guard || guarded_table[i].guard()) {
                   if (guarded_table[i].action) {
                       guarded_table[i].action();
                   }
                   self->current_state = guarded_table[i].next_state;
                   return;
               }
           }
       }
   }

Time-Based Transitions
-----------------------

.. code-block:: c

   typedef struct {
       State base_state;
       uint32_t timeout_ms;
       uint32_t entry_time;
       State timeout_state;
   } TimedState;
   
   void TimedState_Entry(TimedState *self) {
       self->entry_time = get_tick_count();
   }
   
   void TimedState_Update(TimedState *self, StateMachine *sm) {
       uint32_t elapsed = get_tick_count() - self->entry_time;
       
       if (elapsed >= self->timeout_ms) {
           sm->current_state = self->timeout_state;
       }
   }
   
   // Example: Auto-timeout after 5 seconds
   TimedState state_waiting = {
       .base_state = STATE_WAITING,
       .timeout_ms = 5000,
       .timeout_state = STATE_TIMEOUT
   };

Event-Driven State Machine
===========================

Event Queue
-----------

.. code-block:: c

   // Event with data
   typedef struct {
       Event type;
       void *data;
       size_t data_size;
   } EventData;
   
   // Event queue
   typedef struct {
       EventData events[EVENT_QUEUE_SIZE];
       uint8_t head;
       uint8_t tail;
       uint8_t count;
   } EventQueue;
   
   void EventQueue_Init(EventQueue *self) {
       self->head = 0;
       self->tail = 0;
       self->count = 0;
   }
   
   bool EventQueue_Post(EventQueue *self, Event type, void *data, size_t size) {
       if (self->count >= EVENT_QUEUE_SIZE) {
           return false;  // Queue full
       }
       
       self->events[self->tail].type = type;
       self->events[self->tail].data = data;
       self->events[self->tail].data_size = size;
       
       self->tail = (self->tail + 1) % EVENT_QUEUE_SIZE;
       self->count++;
       
       return true;
   }
   
   bool EventQueue_Get(EventQueue *self, EventData *event) {
       if (self->count == 0) {
           return false;  // Queue empty
       }
       
       *event = self->events[self->head];
       self->head = (self->head + 1) % EVENT_QUEUE_SIZE;
       self->count--;
       
       return true;
   }

Event-Driven Loop
-----------------

.. code-block:: c

   EventQueue event_queue;
   StateMachine state_machine;
   
   void event_loop(void) {
       EventQueue_Init(&event_queue);
       StateMachine_Init(&state_machine);
       
       while (1) {
           EventData event;
           
           // Wait for event (can be blocking or timeout-based)
           if (EventQueue_Get(&event_queue, &event)) {
               StateMachine_ProcessEvent(&state_machine, event.type);
           }
           
           // Can also poll for events
           poll_buttons(&event_queue);
           poll_timers(&event_queue);
           poll_communications(&event_queue);
       }
   }
   
   // Post events from ISRs or other tasks
   void button_isr(void) {
       EventQueue_Post(&event_queue, EVENT_BUTTON_PRESS, NULL, 0);
   }

Orthogonal Regions
------------------

.. code-block:: c

   // Multiple concurrent state machines
   typedef struct {
       StateMachine communication;  // Communication state
       StateMachine processing;     // Data processing state
       StateMachine display;        // Display state
   } OrthogonalStateMachine;
   
   void OrthogonalStateMachine_ProcessEvent(OrthogonalStateMachine *self, Event event) {
       // Dispatch to all orthogonal regions
       StateMachine_ProcessEvent(&self->communication, event);
       StateMachine_ProcessEvent(&self->processing, event);
       StateMachine_ProcessEvent(&self->display, event);
   }

Best Practices
==============

1. **Keep states simple** - single responsibility
2. **Use hierarchical states** for shared behavior
3. **Centralize event handling** with event queue
4. **Document state diagrams** - use UML
5. **Test all transitions** - coverage testing
6. **Guard critical transitions** with conditions
7. **Handle unexpected events** gracefully
8. **Use timeouts** to prevent stuck states
9. **Log state changes** for debugging
10. **Profile state machine** overhead

Common Patterns
===============

.. code-block:: c

   // Singleton state machine
   static StateMachine *get_state_machine(void) {
       static StateMachine sm;
       static bool initialized = false;
       
       if (!initialized) {
           StateMachine_Init(&sm);
           initialized = true;
       }
       
       return &sm;
   }
   
   // State machine with context
   typedef struct {
       StateMachine sm;
       uint32_t counter;
       float temperature;
       bool flag;
   } ContextStateMachine;
   
   // Reusable state machine factory
   StateMachine *create_button_sm(void) {
       StateMachine *sm = malloc(sizeof(StateMachine));
       StateMachine_Init(sm);
       return sm;
   }

Quick Reference
===============

.. code-block:: c

   // Simple FSM
   StateMachine sm;
   StateMachine_Init(&sm);
   StateMachine_ProcessEvent(&sm, EVENT_START);
   
   // Table-driven FSM
   // Define transition_table[]
   // Process using table lookup
   
   // HSM
   HSM hsm;
   HSM_Init(&hsm, &state_initial);
   HSM_Dispatch(&hsm, EVENT_START);
   
   // Event queue
   EventQueue_Post(&queue, EVENT_BUTTON, NULL, 0);
   EventQueue_Get(&queue, &event);

See Also
========

- Embedded_Design_Patterns_Behavioral.rst (Strategy, Command patterns)
- Embedded_Design_Patterns_Concurrency.rst (Event queues, message passing)
- Languages/Embedded_C.rst (Function pointers, structures)

References
==========

- UML State Machine Diagrams specification
- Design Patterns for Embedded Systems in C (Bruce Powel Douglass)
- Practical UML Statecharts in C/C++ (Miro Samek)
- Quantum Platform (QP) framework
