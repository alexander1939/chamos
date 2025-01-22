document.addEventListener('DOMContentLoaded', function () {
    function adjustBreadcrumbs() {
        const breadcrumbs = document.querySelectorAll('.breadcrumbsx-item .breadcrumbsx-text');
        const isMobile = window.innerWidth <= 768;

        breadcrumbs.forEach((crumb, index) => {
            if (!crumb.dataset.originalText) {
                crumb.dataset.originalText = crumb.textContent;
            }

            if (isMobile) {
                if (index < breadcrumbs.length - 1) {
                    crumb.textContent = crumb.dataset.originalText.substring(0, 1) + "...";
                }
            } else {
                crumb.textContent = crumb.dataset.originalText;
            }
        });
    }

    adjustBreadcrumbs();

    window.addEventListener('resize', adjustBreadcrumbs);
});
