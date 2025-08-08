from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, FloatField, BooleanField, SubmitField, DateTimeField
from wtforms.validators import DataRequired, Optional, Length, NumberRange

freq_dict = {
    0: "2.5MHz",
    1: "5MHz",
    2: "10MHz",
    3: "20MHz",
    4: "10/20/40MHz",
    5: "40MHz",
    6: "300KHz",
    7: "30MHz",
    8: "1.25MHz",
    9: "250KHz",
    10: "500KHz",
    11: "1MHz"
}

class DeviceStatusForm(FlaskForm):
    """
    用于展示和提交 MimoMesh 设备状态和配置的 FlaskForm。只读字段。
    """
    # 基本信息 (只读字段)
    name = StringField('节点名称', render_kw={'readonly': True})
    ip = StringField('设备 IP', render_kw={'readonly': True})
    selfId = IntegerField('自身 ID', render_kw={'readonly': True})
    nodeNumber = IntegerField('节点数量', render_kw={'readonly': True})
    batteryLevel = FloatField('电池电量 (%)', render_kw={'readonly': True})
    temp = FloatField('设备温度 (°C)', render_kw={'readonly': True})
    silenced = BooleanField('是否静默', render_kw={'readonly': True})
    freq = FloatField('设备频率', render_kw={'readonly': True})
    span = StringField('信道带宽 (MHz)', render_kw={'readonly': True})
    # 提交按钮
    submit = SubmitField('保存配置')
