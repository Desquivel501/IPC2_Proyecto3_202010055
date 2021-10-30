
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
