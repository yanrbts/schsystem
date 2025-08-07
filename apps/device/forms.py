from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, FloatField, BooleanField, SubmitField, SelectField
from wtforms.validators import DataRequired, Optional

class DeviceStatusForm(FlaskForm):
    """
    用于展示和提交 MimoMesh 设备状态和配置的 FlaskForm。
    包含可编辑和只读字段。
    """
    # 基本信息 (只读字段)
    ip = StringField('设备 IP', render_kw={'readonly': True})
    selfId = IntegerField('自身 ID', render_kw={'readonly': True})
    nodeNumber = IntegerField('节点数量', render_kw={'readonly': True})
    
    # 设备状态 (只读字段)
    batteryLevel = FloatField('电池电量 (%)', render_kw={'readonly': True})
    temp = FloatField('设备温度 (°C)', render_kw={'readonly': True})
    
    # 可修改字段
    silenced = BooleanField('是否静默') # 可通过复选框修改
    configUpdated = BooleanField('配置已更新', render_kw={'readonly': True}) # 状态字段，只读

    # 网络配置 (可修改字段)
    nwMask = StringField('网络掩码')
    dnsServer = StringField('DNS 服务器')
    gateway = StringField('网关')
    operatingFreq = IntegerField('操作频率')
    operatingCtrlFreqMask = StringField('操作控制频率掩码', render_kw={'readonly': True}) # 复杂掩码，通常只读

    # 噪音 RSSI 选择字段
    # choices 将在路由中动态填充，coerce=int 确保选中的值是整数类型
    noiseRssiSelect = SelectField('噪音 RSSI', choices=[], coerce=int) 

    # 提交按钮
    submit = SubmitField('保存配置')
