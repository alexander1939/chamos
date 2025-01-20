document.addEventListener('DOMContentLoaded', function () {
    function adjustBreadcrumbs() {
        const breadcrumbs = document.querySelectorAll('.breadcrumbsx-item .breadcrumbsx-text');
        const isMobile = window.innerWidth <= 768;

        breadcrumbs.forEach((crumb, index) => {
            if (isMobile) {
                if (index < breadcrumbs.length - 1) {
                    crumb.textContent = crumb.textContent.substring(0, 1) + "...";
                }
            } else {
                crumb.textContent = crumb.textContent.trim();
            }
        });
    }
    adjustBreadcrumbs();

    window.addEventListener('resize', adjustBreadcrumbs);
});
