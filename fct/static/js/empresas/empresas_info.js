'use strict';


//DOM:
let cuerpoTabla;
let thEmpresa;
let thLocalidad;
let thFPB1;
let thFPB2;
let thSMR;
let thASIR;
let thDAM;
let thDAW;

//VARIABLES GLOBALES:

let ordenamientos= {
        "nombreSort" : true,
        "localidadSort" : true,
        "FPB_IO_1" : false,
        "FPB_IO_2" : false,
        "SMR" : false,
        "ASIR" : false,
        "DAM" : false,
        "DAW" : false
    }


let empresas = [];

document.addEventListener('DOMContentLoaded',(e)=>{
   main();
});

/**
 * Fucnión que se ejecuta cuando se carga el DOM
 * @returns {Promise<void>}
 */
async function main(){
    cargarDOM();
    limpiarContenedor(cuerpoTabla);
    //Obtenemos las empresas y las colocamos:
    empresas = await obtenerEmpresas();
    colocarEmpresas("nombre");


    //Pulsar TH --> Ordenar:

}

/**
 * Coloca las empresas según criterio de ordenamiento
 * -null : Sin criterio
 * - "nombre": Por nombre
 * @param criterioOrdenamiento
 */
function colocarEmpresas(criterioOrdenamiento){
    limpiarContenedor(cuerpoTabla);
    switch (criterioOrdenamiento){
        case "nombre":
            empresas.sort((empresa1, empresa2) => empresa1.empresa.nombre_empresa.localeCompare(empresa2.empresa.nombre_empresa));
            ordenamientos.nombreSort = !ordenamientos.nombreSort;
            if(ordenamientos.nombreSort){ empresas.reverse()}
            break;
        case "localidad":
            empresas.sort((empresa1, empresa2) => empresa1.empresa.localidad_empresa.localeCompare(empresa2.empresa.localidad_empresa));
            ordenamientos.localidadSort = !ordenamientos.localidadSort;
            if(ordenamientos.localidadSort){ empresas.reverse()}
            break;
        default:
            if(criterioOrdenamiento!=null){
                empresas.sort((empresa1, empresa2) => empresa1[criterioOrdenamiento] -empresa2[criterioOrdenamiento]);
                ordenamientos[criterioOrdenamiento] = !ordenamientos[criterioOrdenamiento];
                if(ordenamientos[criterioOrdenamiento]){ empresas.reverse()}
            }
            break;
    }
    for(let empresa of empresas){
        cuerpoTabla.append(empresaTR(empresa));
    }
}


/**
 * Carga los elementos del DOM que necesitamos
 */
function cargarDOM(){
    cuerpoTabla = document.querySelector('#cuerpoTablaEmpresas');
    thEmpresa = document.querySelector('#tabla_empresas th:nth-child(1)');
    thEmpresa.addEventListener('click',()=>{colocarEmpresas("nombre")});

    thLocalidad = document.querySelector('#tabla_empresas th:nth-child(3)');
    thLocalidad.addEventListener('click',()=>{colocarEmpresas("localidad")});

    thFPB1 = document.querySelector('#tabla_empresas th:nth-child(4)');
    thFPB1.addEventListener('click',()=>{colocarEmpresas("FPB_IO_1")});

    thFPB2 = document.querySelector('#tabla_empresas th:nth-child(5)');
    thFPB2.addEventListener('click',()=>{colocarEmpresas("FPB_IO_2")});

    thSMR = document.querySelector('#tabla_empresas th:nth-child(6)');
    thSMR.addEventListener('click',()=>{colocarEmpresas("SMR")});

    thASIR = document.querySelector('#tabla_empresas th:nth-child(7)');
    thASIR.addEventListener('click',()=>{colocarEmpresas("ASIR")});

    thDAM = document.querySelector('#tabla_empresas th:nth-child(8)');
    thDAM.addEventListener('click',()=>{colocarEmpresas("DAM")});

    thDAW = document.querySelector('#tabla_empresas th:nth-child(9)');
    thDAW.addEventListener('click',()=>{colocarEmpresas("DAW")});
}


/**
 * Devuelve el array de empresas del servidor
 * @returns {Promise<any>}
 */
async function obtenerEmpresas(){
    return fetch("/api/empresas/").then(resp=>resp.json())
}

/**
 * Dada una empresa del servidor, nos devuelve su representación como tr de html
 * @param empresa
 */
function empresaTR(empresa){
    let trEmpresa = document.createElement('tr');
    console.log(empresa);
    trEmpresa.innerHTML = `<tr>
                        <td><a href="/fct/empresa/${empresa.empresa.id}/">${empresa.empresa.nombre_empresa}</a></td>
                        <td>
                            ${cursosDeEmpresa(empresa)}   
                        </td>
                        <td>${sanearMayusculasMinusculas(empresa.empresa.localidad_empresa)}</td>
                        <td>${empresa.FPB_IO_1}</td>
                        <td>${empresa.FPB_IO_2}</td>
                        <td>${empresa.SMR}</td>
                        <td>${empresa.ASIR}</td>
                        <td>${empresa.DAM}</td>
                        <td>${empresa.DAW}</td>
                    </tr>`;
    return trEmpresa
}


/**
 * Devuelve una cadena html que representa los cursos de la empresa.
 * @param empresa
 */
function cursosDeEmpresa(empresa){
    let htmlCursos = "";
    for (let curso of empresa.cursos){
        htmlCursos += `<p>${curso.curso_academico} - ${esMarzoOSeptiembre(curso)}</p>`
    }
    return htmlCursos;
}

/**
 * Dado un curso nos dice si tuvo lugar en Marzo o en Junio
 * @param curso
 */
function esMarzoOSeptiembre(curso){
    let mes = +curso.inicio_realizacion_fct.split("-")[1];
    if(mes <=7){
        return "Marzo";
    }
    return "Septiembre";
}

/**
 * Elimina todos los hijos de un contenedor
 * @param contenedor
 */
function limpiarContenedor(contenedor){
    while(contenedor.firstElementChild!=null){
        contenedor.firstElementChild.remove()
    }
}


function sanearMayusculasMinusculas(cadena){
    return cadena.charAt(0).toUpperCase() + cadena.slice(1).toLowerCase();
}