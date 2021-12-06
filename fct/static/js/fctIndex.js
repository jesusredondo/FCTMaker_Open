'use strict';

//BÚSQUEDA:


let busquedas = document.querySelectorAll("[data-search*=buscaAlumnos]");

busquedas.forEach(
    b => b.addEventListener("input",buscaAlumnos)
);


function buscaAlumnos(event) {
    let contenedorAlumnos = document.querySelector("[id="+this.getAttribute("data-search")+"]");
    let hijos = contenedorAlumnos.children;
    for (let i=0; i<hijos.length;i++){
        if(!new RegExp(this.value, 'ig').test(hijos[i].innerHTML)){
            hijos[i].classList.add("d-none");
        }
        else{
            hijos[i].classList.remove("d-none");
        }
    }
}



//Focus al click sobre profesor.

let cabeceros = document.querySelectorAll("div.card-header");
for(let cabecero of cabeceros){
    cabecero.addEventListener("click",function(event){
        setTimeout(()=>{
            this.parentElement.querySelector("input.form-control").focus();
        },50);
    });
}


// Selecciones de tutor y curso:
document.querySelector('#selectorTutor').addEventListener('change',function (evn) {
   fetch('/ajax/getCursosTutorID?tutorID='+this.value)
       .then(response=>response.text())
       .then(text=> document.querySelector('#selectorCurso').innerHTML = text)
       .then(() => actualizarAlumnosCurso());

});


function actualizarAlumnosCurso(){
    if(document.querySelector('#selectorCurso').value !='none') {
        fetch('/ajax/getAlumnosCursoID?cursoID=' + document.querySelector('#selectorCurso').value)
            .then(response => response.text())
            .then(text => document.querySelector('#buscaAlumnos').innerHTML = text)
    }else{
        document.querySelector('#buscaAlumnos').innerHTML = '';
    }
}

document.querySelector('#selectorCurso').addEventListener('change',function (evn) {
  actualizarAlumnosCurso();
});


//ACTUALIZAMOS EL TUTOR AL INICIO: TODO: Rehacer mediante relaciones de tablas, esto es una chapuza.
let nombreTutor = document.querySelector('#userHidden').getAttribute('nombre');
let apellidosTutor = document.querySelector('#userHidden').getAttribute('apellidos');
//recorro los nodos del selector:
let selectValueTutor = document.querySelector('#selectorTutor').firstElementChild;
while(selectValueTutor){
    if(selectValueTutor.innerHTML.includes(nombreTutor) && selectValueTutor.innerHTML.includes(apellidosTutor)){
        selectValueTutor.selected = true;
        console.log(selectValueTutor);
        document.querySelector('#selectorTutor').dispatchEvent(new Event('change'));
        break;
    }
    selectValueTutor = selectValueTutor.nextElementSibling;

}



