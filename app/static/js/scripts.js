
function getCookie(name) {
    if (!document.cookie) {
      return null;
    }
    const token = document.cookie.split(';')
      .map(c => c.trim())
      .filter(c => c.startsWith(name + '='));

    if (token.length === 0) {
      return null;
    }
    return decodeURIComponent(token[0].split('=')[1]);
  }

function ayuda(){
  Swal.fire({
    icon: 'info',
    title: 'Datos del Estudiante',
    html: 'Derek Esquivel Diaz<br>Carnet: 202010055<br>IPC2 Seccion B<br>Segundo Semestre 2021'
  })
}   


function saveAsPDF() {
  var doc = new jsPDF("l", "mm", "a4");

  var canvas = document.getElementById('myChart');
  var dataURL = canvas.toDataURL();
  const imgProps = doc.getImageProperties(dataURL);

  var width = doc.internal.pageSize.getWidth() - 20;
  var height = (imgProps.height * width) / imgProps.width;

  doc.addImage(dataURL, 'JPEG', 10, 10, width, height);
  doc.save('graph.pdf');
}


function cargaArchivo(){
  let archivo = document.getElementById('file').files[0];
  var texto = ""
  
  const reader = new FileReader();
  reader.readAsText(archivo, "UTF-8");
  reader.onload = function() {
    console.log(reader.result);
    document.getElementById('entrada').value = reader.result
  };
}

function borrar(){
  
  Swal.fire({
    title: '¿Desea eliminar todos los registros?',
    showDenyButton: true,
    
    confirmButtonText: 'Si',
    denyButtonText: 'No',
    customClass: {
      actions: 'my-actions',
      cancelButton: 'order-1 right-gap',
      confirmButton: 'order-2',
      denyButton: 'order-3',
    }
  }).then((result) => {
    if (result.isConfirmed) {
      document.getElementById('entrada').value = ""
      document.getElementById('salida').value = ""

      fetch('http://127.0.0.1:8000/reset', {
        method: 'GET'

        })
        .then(res => res.json())
        .catch(err =>{
            console.log("Ha ocurrido un error");
            alert("Ha ocurrido un error")
        })
          .then(response =>{
            
        })
      Swal.fire('Borrado!', '', 'success')
    } else if (result.isDenied) {
      
    }
  })

  
}

function getSalida(){
  fetch('http://127.0.0.1:8000/getSalida', {
  method: 'GET',
  })
  .then(res => res.json())
  .catch(err =>{
      console.log("Ha ocurrido un error");
      alert("Ha ocurrido un error")
  })
    .then(response =>{
      document.getElementById('salida').value = response.xml
  })
}

function dataPDF(){

  var doc = new jsPDF("l", "mm", "a4");
  var height = doc.internal.pageSize.height
  doc.setFontSize(12)

  fetch('http://127.0.0.1:8000/getSalida', {
      method: 'GET',
    })
    .then(res => res.json())
    .catch(err =>{
      console.log("Ha ocurrido un error");
      alert("Ha ocurrido un error")
    })
    .then(response =>{

      array_lineas = response.xml.split("\n")
      y = 0
      cont = 0
      for( i in array_lineas){
        doc.text(array_lineas[i], 10, 10 + y )
        y = y + 5
        cont += 1
        if (cont > 38){
          doc.addPage();
          y = 0
          cont = 0
        }
      }
      doc.save("autorizaciones.pdf")

    })
}