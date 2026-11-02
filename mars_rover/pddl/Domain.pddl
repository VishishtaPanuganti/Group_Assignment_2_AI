;; Mars Rover Sample Collection - Domain (STRIPS + typing only)
(define (domain mars-rover)
  (:requirements :strips :typing)

  (:types
    location
    rover
    bay
    drill
    rock
  )

  (:predicates
    (rover-at ?v - rover ?l - location)          ; rover position
    (connected ?from ?to - location)             ; DIRECTED edge (two-way routes = two facts)
    (rock-at ?r - rock ?l - location)            ; rock lying at a location
    (drill-at ?d - drill ?l - location)          ; drill lying at a location
    (has-drill ?v - rover ?d - drill)            ; rover carries the drill (permanent)
    (soft ?r - rock)                             ; soft rock: no drill needed
    (hard ?r - rock)                             ; hard rock: drill needed
    (bay-of ?b - bay ?v - rover)                 ; bay belongs to rover
    (bay-empty ?b - bay)                         ; bay holds nothing
    (in-bay ?r - rock ?b - bay)                  ; rock stored in bay
  )

  ;; Move along a directed edge. A two-way route has two connected facts;
  ;; the one-way slope SiteC -> SiteD has only one.
  (:action move
    :parameters (?v - rover ?from ?to - location)
    :precondition (and (rover-at ?v ?from) (connected ?from ?to))
    :effect (and (rover-at ?v ?to) (not (rover-at ?v ?from)))
  )

  (:action pick-drill
    :parameters (?v - rover ?d - drill ?l - location)
    :precondition (and (rover-at ?v ?l) (drill-at ?d ?l))
    :effect (and (has-drill ?v ?d) (not (drill-at ?d ?l)))
  )

  (:action collect-soft
    :parameters (?v - rover ?r - rock ?l - location ?b - bay)
    :precondition (and (rover-at ?v ?l) (rock-at ?r ?l) (soft ?r)
                       (bay-of ?b ?v) (bay-empty ?b))
    :effect (and (in-bay ?r ?b) (not (rock-at ?r ?l)) (not (bay-empty ?b)))
  )

  (:action collect-hard
    :parameters (?v - rover ?r - rock ?l - location ?b - bay ?d - drill)
    :precondition (and (rover-at ?v ?l) (rock-at ?r ?l) (hard ?r)
                       (has-drill ?v ?d) (bay-of ?b ?v) (bay-empty ?b))
    :effect (and (in-bay ?r ?b) (not (rock-at ?r ?l)) (not (bay-empty ?b)))
  )

  (:action deposit
    :parameters (?v - rover ?r - rock ?l - location ?b - bay)
    :precondition (and (rover-at ?v ?l) (in-bay ?r ?b) (bay-of ?b ?v))
    :effect (and (rock-at ?r ?l) (bay-empty ?b) (not (in-bay ?r ?b)))
  )
)
