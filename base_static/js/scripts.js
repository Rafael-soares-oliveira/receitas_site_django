function confirm_delete(params) {
    const forms = document.querySelectorAll(".form-delete");
    for (const form of forms) {
        form.addEventListener('submit', function(e) {
            e.preventDefault();
            const confirmed = confirm('Are you sure you want to delete?')
            if (confirmed) {
                form.submit();
            }
        });
    }
}
confirm_delete()

function unpublish_recipe() {
    const forms = document.querySelectorAll(".form-unpublish");
    for (const form of forms) {
        form.addEventListener('submit', function(e) {
            e.preventDefault();
            const confirmed = confirm('Are you sure you want to unpublish?')
            if (confirmed) {
                form.submit();
            }
        });
    }
}
unpublish_recipe()

function menu() {
    const buttonCloseMenu = document.querySelector('.button-close-menu');
    const buttonShowMenu = document.querySelector('.button-show-menu');
    const menuContainer = document.querySelector('.menu-container');
  
    const buttonShowMenuVisibleClass = 'button-show-menu-visible';
    const menuHiddenClass = 'menu-hidden';
  
    const closeMenu = () => {
      buttonShowMenu.classList.add(buttonShowMenuVisibleClass);
      menuContainer.classList.add(menuHiddenClass);
    };
  
    const showMenu = () => {
      buttonShowMenu.classList.remove(buttonShowMenuVisibleClass);
      menuContainer.classList.remove(menuHiddenClass);
    };
  
    if (buttonCloseMenu) {
      buttonCloseMenu.removeEventListener('click', closeMenu);
      buttonCloseMenu.addEventListener('click', closeMenu);
    }
  
    if (buttonShowMenu) {
      buttonCloseMenu.removeEventListener('click', showMenu);
      buttonShowMenu.addEventListener('click', showMenu);
    }
  };

menu()