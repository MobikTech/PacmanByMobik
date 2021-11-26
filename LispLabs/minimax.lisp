(defparameter road 0)
(defparameter wall 1)
(defparameter player (list 0 2))
(defparameter enemy (list 3 2))

(defun generate-game-field ()
  (let (
        (field (make-array '(5 5)) )
        )
    (dotimes (i 5)
      (dotimes (k 5)
        (setf (aref field i k) (random 2))
        )
      )
    (return-from generate-game-field field)
))

(defparameter game-field (generate-game-field))




(defun get-neighbors (field x y)
  (let (
        (coords-list ()))
    (when (and (>= (- x 1) 0) (/= (aref field (- x 1) y) wall))
      (setq coords-list (append coords-list (list (list (- x 1) y)))))

    (when (and (< (+ x 1) 5) (/= (aref field (+ x 1) y) wall))
      (setq coords-list (append coords-list (list (list (+ x 1) y)))))

    (when (and (>= (- y 1) 0) (/= (aref field x (- y 1)) wall))
      (setq coords-list (append coords-list (list (list x (- y 1))))))

    (when (and (< (+ y 1) 5) (/= (aref field x (+ y 1)) wall))
      (setq coords-list (append coords-list (list (list x (+ y 1))))))

    (return-from get-neighbors coords-list)
    )
  )


(defun evaluate (player-x player-y enemy-x enemy-y)
  (let (
        (evaluation 0))
    (setq evaluation (sqrt (+
                            (expt (- enemy-x player-x) 2)
                            (expt (- enemy-y player-y) 2)
                            )))
    (return-from evaluate evaluation)
    )
  )

(defun minimax (field maximize player-x player-y enemy-x enemy-y)
  (let (
        (neighbors ())
        (evaluation 0)
        (current-max 10000)
        (current-min -10000)
        (best-coords ())
        (enemy-coords ())
        )

    (if maximize
        (progn
          (setq best-coords (list player-x player-y))
         (setq neighbors (get-neighbors field player-x player-y))
         (dolist (coords neighbors)  
           (setq enemy-coords (minimax field nil (nth 0 coords) (nth 1 coords) enemy-x enemy-y))
           (setq evaluation (evaluate (nth 0 coords) (nth 1 coords) (nth 0 enemy-coords) (nth 1 enemy-coords)))
           (when (> evaluation current-min)
             (progn
               (setq current-min evaluation)
               (setq best-coords coords)))
           )
         (return-from minimax best-coords)
         )
        (progn
         (setq best-coords (list enemy-x enemy-y))
         (setq neighbors (get-neighbors field enemy-x enemy-y))
         (dolist (coords neighbors)
           (setq evaluation (evaluate (nth 0 coords) (nth 1 coords) player-x player-y))
           (when (< evaluation current-max)
             (progn
               (setq current-min evaluation)
               (setq best-coords coords)))
           )
         (return-from minimax best-coords)
         )
       )))


(terpri)
(write game-field)
(terpri)
(write (minimax game-field t 0 2 3 2))
