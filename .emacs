(custom-set-variables
  ;; custom-set-variables was added by Custom -- don't edit or cut/paste it!
  ;; Your init file should contain only one such instance.
 '(column-number-mode t)
 '(make-backup-files nil)
 '(menu-bar-mode nil)
 '(pc-select-meta-moves-sexps t)
 '(pc-select-selection-keys-only t)
 '(pc-selection-mode t nil (pc-select))
 '(tab-stop-list (quote (4 8 12 16 20 24 28 32 36 40 44 48 52 56 60 64 68 72 76 80 84 88 92 96 100 104 108 112 116 120)))
 '(tool-bar-mode nil nil (tool-bar))
 '(tooltip-mode nil nil (tooltip))
 '(widget-menu-max-size 0))


; '(tool-bar-mode nil nil (tool-bar))
; '(tooltip-mode nil nil (tooltip))

(custom-set-faces
  ;; custom-set-faces was added by Custom -- don't edit or cut/paste it!
  ;; Your init file should contain only one such instance.
 )
(setq ispell-program-name "/sw/bin/ispell")
(put 'upcase-region 'disabled nil)
(set-background-color "white")
(global-font-lock-mode 1)
(set-foreground-color "turquoise")
(set-foreground-color "black")
(set-cursor-color "white")
(set-face-background 'region "dark green")
(set-face-foreground 'region "black")
(make-face 'paren-match-face)
(set-face-foreground 'paren-match-face "White")
(set-face-background 'paren-match-face "Black")
(setq show-paren-face 'paren-match-face)
(setq auto-mode-alist
      (cons '("\\.h$" . c++-mode) (cons '("\\.py$" . python-mode) auto-mode-alist)))
(setq interpreter-mode-alist
      (cons '("python" . python-mode)
            interpreter-mode-alist))
(setq load-path (cons "C:\Program Files\emacs-20.7\lisp" load-path))
(autoload 'python-mode "python-mode" "Python editing mode." t)
(defun mouse-wheel-backward nil (interactive) (scroll-down 10))
(defun mouse-wheel-forward nil (interactive) (scroll-up 10))

(global-set-key [(mouse-4)] 'mouse-wheel-backward)
(global-set-key [(mouse-5)] 'mouse-wheel-forward)
(setq inferior-lisp-program "/users/daniel/Applications/acl62_trial/alisp")
(global-set-key "\C-x\C-l" 'run-lisp)
(global-set-key "\C-xd" 'lisp-eval-defun)
(global-set-key "\C-x\C-d" 'lisp-eval-defun-and-go)
(global-set-key "\M-g" 'goto-line)
(font-lock-mode)


(setq c-indent-level 4)
(setq c-basic-offset 4)


(defconst my-c-style
  '((c-tab-always-indent        . t)
    (c-comment-only-line-offset . 4)
    )
  "My C Programming Style")

(defun my-c-mode-common-hook ()
  (c-add-style "PERSONAL" my-c-style t)
  (c-set-offset 'member-init-intro '++)
  ;; other customizations
  (setq tab-width 4
        indent-tabs-mode t)
  ;; we like auto-newline and hungry-delete
  ;(c-toggle-auto-hungry-state 1)
  ;; keybindings for all supported languages.  We can put these in
  ;; c-mode-base-map because c-mode-map, c++-mode-map, objc-mode-map,
  ;; java-mode-map, and idl-mode-map inherit from it.
  (define-key c-mode-base-map "\C-m" 'newline-and-indent)
  )

(add-hook 'c-mode-common-hook 'my-c-mode-common-hook)