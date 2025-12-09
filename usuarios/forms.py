from django import forms
from django.contrib.auth import authenticate


class LoginForm(forms.Form):
    """
    Formulario de inicio de sesión
    """
    username = forms.CharField(
        label='Usuario',
        max_length=150,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ingresa tu usuario',
            'autofocus': True
        })
    )
    
    password = forms.CharField(
        label='Contraseña',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ingresa tu contraseña'
        })
    )
    
    def clean(self):
        """
        Validación personalizada: verificar que las credenciales sean correctas
        """
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')
        
        if username and password:
            # Intentar autenticar
            user = authenticate(username=username, password=password)
            
            if user is None:
                # Credenciales incorrectas
                raise forms.ValidationError('Usuario o contraseña incorrectos')
            
            # Guardar el usuario autenticado en el formulario para usarlo después
            self.user = user
        
        return cleaned_data
