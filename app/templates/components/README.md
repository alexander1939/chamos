**⚠️ Advertencia:** Asegúrate de importar correctamente el componente antes de usarlo, ya que de lo contrario se generará un error.

{% from 'components/nombre_del_componente.jinja' import nombre_del_macro %}




## 1. Componente: `seccion_option.jinja`

Este componente está diseñado para generar una lista de enlaces que representan diferentes secciones dentro de una página. Es útil para mostrar un menú de opciones que dirigen al usuario a diversas áreas de la misma página o a otras páginas.

### Funcionalidad:
El macro `sections_per` recibe una lista de objetos que contienen el nombre y la URL de cada sección. Crea una lista de secciones, con cada elemento representado como un enlace.

### Parámetros:
- `sections`: Una lista de objetos, donde cada objeto debe contener los atributos:
  - `name`: El nombre de la sección.
  - `url`: El enlace a la sección.

### ejemplo:
{% from 'components/seccion_option.jinja' import sections_per %}

{% set sections = [
    {'name': 'Sección 1', 'url': '/seccion1'},
    {'name': 'Sección 2', 'url': '/seccion2'}
] %}

{{ sections_per(sections) }}




## 2. Componente: `proyectos_section.jinja`

Este componente permite crear una sección con un título, subtítulo y una lista de materias o proyectos. Cada materia o proyecto incluye un nombre, descripción y un enlace para obtener más información.

### Funcionalidad:
El macro `proyectos_section` recibe tres parámetros: un título para la sección, un subtítulo para proporcionar más contexto, y una lista de materias o proyectos. Cada materia o proyecto contiene un nombre, una descripción y un enlace para obtener más información.

### Parámetros:
- `title`: El título principal de la sección.
- `subtitle`: Un subtítulo que proporciona más información sobre la sección.
- `materias`: Una lista de objetos, donde cada objeto debe contener los atributos:
  - `name`: El nombre de la materia o proyecto.
  - `description`: Una breve descripción de la materia o proyecto.
  - `url`: Un enlace a la página con más detalles sobre la materia o proyecto.

### ejemplo:

{% from 'components/section_option-list.jinja' import proyectos_section %}

{% set materias = [
    {'name': 'Matemáticas', 'description': 'Descripción de matemáticas', 'url': '#'},
    {'name': 'Física', 'description': 'Descripción de física', 'url': '#'}
] %}

{{ proyectos_section('Proyectos de Estudio', 'Lista de materias', materias) }}