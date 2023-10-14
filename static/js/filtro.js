document.addEventListener("DOMContentLoaded", function() {
  const filterButton = document.getElementById("filter-button");
  const filterOptions = document.getElementById("filter-options");
  const categorias = document.querySelectorAll(".category-filter");
  const todasLasCategorias = document.getElementById("all-categories");
  const categoriaDescription = document.getElementById("categoria-description");

  let optionsVisible = false; // Variable para controlar la visibilidad de las opciones

  filterButton.addEventListener("click", function(event) {
      event.preventDefault();
      optionsVisible = !optionsVisible; // Alternar la visibilidad
      filterOptions.style.display = optionsVisible ? "block" : "none"; // Mostrar u ocultar según el estado
  });

  todasLasCategorias.addEventListener("click", function(event) {
      event.preventDefault();
      mostrarTodasLasPublicaciones();
      ocultarOpciones();
      const publicaciones = document.querySelectorAll(".en_progreso");
      if (publicaciones.length === 0) {
          categoriaDescription.textContent = "No tienes publicaciones disponibles.";
          categoriaDescription.style.display = "block";
      } else {
          ocultarDescripcion();
      }
  });

  categorias.forEach(function(categoria) {
      categoria.addEventListener("click", function(event) {
          event.preventDefault();
          const categoriaId = categoria.getAttribute("data-categoria");
          const categoriaNombre = categoria.textContent;

          ocultarTodasLasTarjetas();

          const publicaciones = document.querySelectorAll(`.en_progreso[data-categoria="${categoriaId}"]`);
          publicaciones.forEach(function(tarjeta) {
              tarjeta.style.display = "block";
          });

          if (publicaciones.length === 0) {
              categoriaDescription.textContent = `No tienes publicaciones con la categoría "${categoriaNombre}".`;
              categoriaDescription.style.display = "block";
          } else {
              ocultarDescripcion();
          }

          ocultarOpciones();
      });
  });

  document.addEventListener("click", function(event) {
      if (!filterButton.contains(event.target)) {
          ocultarOpciones();
      }
  });

  function ocultarOpciones() {
      optionsVisible = false;
      filterOptions.style.display = "none";
  }

  function ocultarTodasLasTarjetas() {
      const tarjetasEnProgreso = document.querySelectorAll(".en_progreso");
      tarjetasEnProgreso.forEach(function(tarjeta) {
          tarjeta.style.display = "none";
      });
  }

  function mostrarTodasLasPublicaciones() {
      const tarjetasEnProgreso = document.querySelectorAll(".en_progreso");
      tarjetasEnProgreso.forEach(function(tarjeta) {
          tarjeta.style.display = "block";
      });
  }

  function ocultarDescripcion() {
      categoriaDescription.style.display = "none";
  }
});
