const mapElement = document.getElementById('map');

if (mapElement) {
    const map = L.map(mapElement, {
        scrollWheelZoom: true
    }).setView([59.9343, 30.3351], 13);

    L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/Canvas/World_Light_Gray_Base/MapServer/tile/{z}/{y}/{x}', {
        maxZoom: 16,
        attribution: 'Tiles © Esri — Esri, DeLorme, NAVTEQ'
    }).addTo(map);
}

const loginModal = document.getElementById('login-modal');
const registerModal = document.getElementById('register-modal');

if (loginModal && registerModal) {
    const modals = [loginModal, registerModal];
    let returnFocus = null;

    function activeModal() {
        return modals.find(modal => !modal.hidden);
    }

    function showModal(modal, rememberFocus = true) {
        if (!modal) return;

        if (rememberFocus && !activeModal()) {
            returnFocus = document.activeElement;
        }

        modals.forEach(item => {
            item.hidden = item !== modal;
        });

        document.body.classList.add('modal-open');

        const firstInput = modal.querySelector('input:not([type="hidden"]):not([type="checkbox"])');
        (firstInput || modal.querySelector('[data-close-modal]'))?.focus();
    }

    function closeModal() {
        modals.forEach(modal => {
            modal.hidden = true;
        });

        document.body.classList.remove('modal-open');

        if (returnFocus && returnFocus.isConnected) {
            returnFocus.focus();
        } else {
            document.getElementById('open-login')?.focus();
        }
    }

    const openLoginButton = document.getElementById('open-login');

    if (openLoginButton) {
        openLoginButton.addEventListener('click', () => {
            showModal(loginModal);
        });
    }

    document.querySelectorAll('[data-switch-modal]').forEach(button => {
        button.addEventListener('click', () => {
            const targetModal = document.getElementById(button.dataset.switchModal);
            showModal(targetModal, false);
        });
    });

    document.querySelectorAll('[data-close-modal]').forEach(button => {
        button.addEventListener('click', closeModal);
    });

    modals.forEach(modal => {
        modal.addEventListener('click', event => {
            if (event.target === modal) {
                closeModal();
            }
        });
    });

    document.addEventListener('keydown', event => {
        const modal = activeModal();

        if (!modal) return;

        if (event.key === 'Escape') {
            closeModal();
            return;
        }

        if (event.key === 'Tab') {
            const elements = [...modal.querySelectorAll('button, a[href], input:not([type="hidden"]), select, textarea')]
                .filter(element => !element.disabled && element.getClientRects().length);

            if (!elements.length) return;

            const first = elements[0];
            const last = elements[elements.length - 1];

            if (event.shiftKey && document.activeElement === first) {
                event.preventDefault();
                last.focus();
            } else if (!event.shiftKey && document.activeElement === last) {
                event.preventDefault();
                first.focus();
            }
        }
    });

    const modalSettings = document.getElementById('modal-settings');

    if (modalSettings?.dataset.registerOpen === 'true') {
        showModal(registerModal);
    } else if (modalSettings?.dataset.loginOpen === 'true') {
        showModal(loginModal);
    }
}
