from flask.ext.wtf import Form, TextField, TextAreaField, SubmitField
 
class SearchForm(Form):
  artist = StringField("artist")