





function validarDatos(){

parrafo = document.getElementById("Error")
pag = document.getElementById("pagina1")
if(document.formulario.nombre.value.length <= 1) {

document.formulario.nombre.focus()
parrafo.innerHTML = "Nombre no valido"
return
}





let edadCazador = parseInt(document.formulario.edad.value)
if(isNaN(edadCazador)) {
  document.formulario.edad.focus()
  parrafo.innerHTML = "Edad incorrecta"
  return
}
 else{
    if(edadCazador  <=0 ){
    document.formulario.edad.focus()
    parrafo.innerHTML = "Imposible"
    return
    }


}

if(document.formulario.experiencia.selectedIndex == 0) {


document.formulario.experiencia.focus()
parrafo.innerHTML = "Por favor elija una opcion."
return


}

parrafo.innerHTML = "Gracias por presentarte."
pag.innerHTML = "Bienvenido al gremio de Cazadores"
document.formualrio.submit()

}