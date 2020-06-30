from flask_wtf import FlaskForm,  RecaptchaField
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo

class SettingsForm(FlaskForm):
    res_x = SelectField('Resolution Width', choices=[1280,1920,3280], validators=[DataRequired()], id="settings_res_x")
    res_y = SelectField('Resolution Height',choices=[720,1080,2464], validators=[DataRequired()], id="settings_res_y")
    rotation = SelectField('Rotation', validators=[DataRequired()],choices=[0, 90, 180, 270], id="settings_rotation")
    effect = SelectField('Effect', choices=['none', 'negative', 'sketch', 'denoise', 'emboss', 'oilpaint', 'hatch', 'gpen', 'pastel', 'watercolor', 'film', 'blur', 'saturation'], id="settings_effect")
    save = SubmitField('Apply', id="save-settings")