with(document.comprar){
	onsubmit = function(e){
		e.preventDefault();
		ok = true;
		if(ok && nombre.value==""){
			ok=false;
			alert("Debe escribir su nombre");
			nombre.focus();
		}
		if(ok && ap_paterno.value==""){
			ok=false;
			alert("Debe escribir su apellido paterno");
			ap_paterno.focus();
		}
		if(ok && ap_materno.value==""){
			ok=false;
			alert("Debe escribir su apellido materno");
			ap_materno.focus();
		}
		if(ok && telefono.value==""){
			ok=false;
			alert("Debe escribir su telefono");
			telefono.focus();
		}
		if(ok && correo.value==""){
			ok=false;
			alert("Debe escribir su correo electronico");
			correo_alt.focus();
		}
		if(ok && calle.value==""){
			ok=false;
			alert("Debe escribir su calle");
			calle.focus();
		}
		if(ok && num.value==""){
			ok=false;
			alert("Debe escribir su numero");
			num.focus();
		}
		if(ok && colonia.value==""){
			ok=false;
			alert("Debe escribir su colonia");
			colonia.focus();
		}
		if(ok && delegacion.value==""){
			ok=false;
			alert("Debe escribir su delegacion");
			delegacion.focus();
		}

		if(ok){ submit(); }
	}
}