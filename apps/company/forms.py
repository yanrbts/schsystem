from flask_wtf import FlaskForm
from wtforms import (
    StringField, 
    IntegerField, 
    FloatField, 
    BooleanField, 
    SubmitField, 
    DateTimeField
)
from wtforms.validators import DataRequired, Optional, Length, NumberRange

class CompanyForm(FlaskForm):
    id = IntegerField('ID')
    create_time = DateTimeField('创建时间', format='%Y-%m-%d %H:%M:%S', validators=[Optional()])
    update_time = DateTimeField('更新时间', format='%Y-%m-%d %H:%M:%S', validators=[Optional()])
    sys_org_code = StringField('组织编码', validators=[Optional(), Length(max=64)])
    
    com_name = StringField('公司名称', validators=[DataRequired(), Length(max=256)])
    district = StringField('行政区', validators=[Optional(), Length(max=32)])
    street = StringField('街道', validators=[Optional(), Length(max=256)])
    size = IntegerField('企业规模', validators=[Optional(), NumberRange(min=0)])
    type = StringField('企业类型', validators=[Optional(), Length(max=32)])
    address = StringField('地址', validators=[Optional(), Length(max=1024)])
    credit_code = StringField('信用代码', validators=[Optional(), Length(max=32)])
    
    lon = FloatField('经度', validators=[
        Optional(),
        NumberRange(min=-180, max=180, message="经度值必须在-180到180之间。")
    ])
    lat = FloatField('纬度', validators=[
        Optional(),
        NumberRange(min=-90, max=90, message="纬度值必须在-90到90之间。")
    ])
    
    submit = SubmitField('保存')
