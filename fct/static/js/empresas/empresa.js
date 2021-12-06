'use strict';

//Elementos del DOM:
let mapaDiv ;

//Elementos del Mapa:
let mapa;
let lat;
let lng;

//Elementos para almacenar el anexo0.


document.addEventListener('DOMContentLoaded', ()=>{
    main();
})


/**
 * Se llama al cargar el DOM.
 * @returns {Promise<void>}
 */
async function main(){
    separarHistoricosBotones()
}


/**
 * Crea un separador <br> entre cada curso:
 */
function separarHistoricosBotones(){
    let ultimas_siglas = '';
    let botonesHistoricos = document.querySelectorAll('.historico-btn');
    for(let botonHistorico of botonesHistoricos){
        let siguienteBotonHistorico = botonHistorico.nextElementSibling;
        let siglas = botonHistorico.innerText.split(" ").pop() //Las siglas como texto al final
        if(siguienteBotonHistorico){
            let siglasSiguiente = siguienteBotonHistorico.innerText.split(" ").pop();
            if(siglas !== siglasSiguiente){
                botonHistorico.insertAdjacentHTML('afterend','<br>')
            }
        }
    }
}


