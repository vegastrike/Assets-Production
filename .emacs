(custom-set-variables
  ;; custom-set-variables was added by Custom -- don't edit or cut/paste it!
  ;; Your init file should contain only one such instance.
 '(line-number-mode t)
 '(query-user-mail-address nil)
 '(standard-indent 3)
 '(tab-stop-list (quote (2 4 6 8 10 12 14 16 18 20 22 24 26 28 30)))
 '(truncate-lines t)
 '(user-mail-address "ianbuck@graphics.Stanford.EDU"))
(custom-set-faces
  ;; custom-set-faces was added by Custom -- don't edit or cut/paste it!
  ;; Your init file should contain only one such instance.
 '(default ((t (:foreground "white" :background "black" :bold nil))))
 '(font-lock-comment-face ((nil (:foreground "green1"))))
 '(font-lock-function-name-face ((((class color) (background light)) (:foreground "brown2" :bold t))))
 '(font-lock-keyword-face ((nil (:foreground "red1" :bold t)))))


;; Load the C++ and C editing modes and specify which file extensions
;; correspond to which modes.

(autoload 'c++-mode "cc-mode" "C++ Editing Mode" t)
(autoload 'c-mode "c-mode" "C Editing Mode"   t)
(setq auto-mode-alist
      (append '(("\\.C\\'" . c++-mode)
                ("\\.cc\\'" . c++-mode)
                ("\\.c\\'" . c-mode)
                ("\\.br\\'" . c++-mode)
                ("\\.h\\'"  . c++-mode))
              auto-mode-alist))

(add-hook 'tex-mode-hook
	  '(lambda ()
	    (auto-fill-mode t)
	    (font-lock-mode t) 
))

(add-hook 'c++-mode-hook
	  '(lambda ()
	    (font-lock-mode t) 
	    (setq-default indent-tabs-mode nil)
;	    (setq c-tab-always-indent nil)
	    (setq-default c-basic-offset 3)
	    (setq c-indent-level 3)
	    (setq c-brace-imaginary-offset 0)
	    (setq c-brace-offset 0)
	    (setq c-label-offset -3)
	    (setq c-continued-statement-offset 3)
	    (setq c-argdecl-indent 3)
	    ))

(global-unset-key "\C-h")
(global-set-key "\C-h" 'backward-delete-char)

