from flask import render_template, redirect, request, url_for, flash, session
from flask_login import current_user, login_user, logout_user
from apps.config import Config
from apps.meshapi import MeshAPI
from apps.device import blueprint
from apps.device.forms import DeviceStatusForm
import json

@blueprint.route("/device", methods=['GET', 'POST'])
def device():
    """ Render the device page and handle form submission """
    form = DeviceStatusForm()
    jsdata = {}

    # 仅在 GET 时访问设备接口
    if request.method == 'GET':
        try:
            msh = MeshAPI(Config.MIMOMESH_BASE_URL)
            jsdata = msh.get_status()
            # 将 jsdata 保存到 session（转换成字符串）
            session['jsdata'] = json.dumps(jsdata)
        except Exception as e:
            flash(f"错误：无法获取设备状态 - {e}", 'error')

    elif request.method == 'POST':
        # 从 session 获取之前的设备状态数据
        try:
            jsdata = json.loads(session.get('jsdata', '{}'))
        except Exception as e:
            flash(f"错误：无法读取设备缓存数据 - {e}", 'error')
            jsdata = {}

    # 填充 noiseRssiSelect 的选项（GET 和 POST 都要）
    if jsdata and 'noiseRssi' in jsdata and jsdata['noiseRssi']:
        form.noiseRssiSelect.choices = [
            (index, f"频率: {entry.get('freq', 'N/A')} Hz")
            for index, entry in enumerate(jsdata['noiseRssi'])
        ]
        if not form.noiseRssiSelect.data and len(form.noiseRssiSelect.choices) > 0:
            form.noiseRssiSelect.data = form.noiseRssiSelect.choices[0][0]
    else:
        form.noiseRssiSelect.choices = [(0, "无噪音 RSSI 数据")]
        form.noiseRssiSelect.data = 0

    # 处理提交
    if request.method == 'POST' and 'save' in request.form:
        updated_data = {
            'silenced': form.silenced.data,
            'nwMask': form.nwMask.data,
            'dnsServer': form.dnsServer.data,
            'gateway': form.gateway.data,
            'operatingFreq': form.operatingFreq.data,
        }

        selected_noise_rssi_index = form.noiseRssiSelect.data
        selected_noise_rssi_freq = None
        if jsdata and 'noiseRssi' in jsdata and selected_noise_rssi_index is not None and 0 <= selected_noise_rssi_index < len(jsdata['noiseRssi']):
            selected_noise_rssi_freq = jsdata['noiseRssi'][selected_noise_rssi_index].get('freq')

        updated_data['selectedNoiseRssiFreq'] = selected_noise_rssi_freq

        print(f"尝试更新的数据: {updated_data}")
        try:
            # 这里可以执行更新设备配置的操作
            flash('设备配置已成功保存！', 'success')
            return redirect(url_for('device_blueprint.device')) 
        except Exception as e:
            flash(f'保存配置失败：{e}', 'error')
            print(f"配置保存失败: {e}")

    elif request.method == 'GET':
        for field_name, value in jsdata.items():
            if hasattr(form, field_name) and field_name != 'noiseRssiSelect':
                form_field = getattr(form, field_name)
                form_field.data = value

    return render_template("device/device.html", form=form, raw_data=jsdata)
