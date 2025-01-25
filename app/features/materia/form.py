from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, IntegerField, SelectField, SubmitField
from wtforms.validators import DataRequired, Length, NumberRange

class MateriaForm(FlaskForm):
    nombre = StringField('Nombre', validators=[DataRequired(), Length(max=100)])
    descripcion = TextAreaField('Descripción', validators=[Length(max=255)])
    docente = StringField('Docente', validators=[DataRequired(), Length(max=120)])
    creditos = IntegerField('Créditos', validators=[DataRequired(), NumberRange(min=1, max=10)])
    semestre = SelectField('Semestre', choices=[
        ('Primero', 'Primero'), ('Segundo', 'Segundo'), ('Tercero', 'Tercero'),
        ('Cuarto', 'Cuarto'), ('Quinto', 'Quinto'), ('Sexto', 'Sexto'),
        ('Séptimo', 'Séptimo'), ('Octavo', 'Octavo'), ('Noveno', 'Noveno')
    ], validators=[DataRequired()])
    submit = SubmitField('Crear Materia')
