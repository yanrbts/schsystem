from flask import render_template, redirect, request, url_for, flash, session
from flask_login import current_user, login_user, logout_user
from apps.config import Config
from apps.meshapi import MeshAPI
from apps.device import blueprint
from apps.device.forms import DeviceStatusForm, freq_dict
from apps.models import Company

@blueprint.route("/device", methods=['GET', 'POST'])
def device():
    """ Render the device page and handle form submission """
    form = DeviceStatusForm()
    jsdata = {}
    jsconfdata = {}
    # 仅在 GET 时访问设备接口
    if request.method == 'GET':
        try:
            with MeshAPI(Config.MIMOMESH_BASE_URL) as msh:
                jsdata = msh.get_status()
                jsconfdata = msh.get_config()
        except Exception as e:
            flash(f"错误：无法获取设备状态 - {e}", 'error')

    if request.method == 'POST' and 'save' in request.form:
        try:
            return redirect(Config.MIMOMESH_BASE_URL)
        except Exception as e:
            flash(f'保存配置失败：{e}', 'error')

    elif request.method == 'GET':
        for field_name, value in jsdata.items():
            if hasattr(form, field_name):
                form_field = getattr(form, field_name)
                form_field.data = value
        for field_name, value in jsconfdata.items():
            if hasattr(form, field_name):
                form_field = getattr(form, field_name)
                form_field.data = value

        form.freq.data = jsconfdata['freqList'][jsdata['operatingFreq']]
        form.span.data = freq_dict.get(jsconfdata['span'], 0)

    return render_template("device/device.html", form=form, raw_data=jsdata)

@blueprint.route("/devlist", methods=['GET'])
def devlist():
    """ Render the device list page """
    node_infos = []
    try:
        with MeshAPI(Config.MIMOMESH_BASE_URL) as msh:
            jsdata = msh.get_status()
            if 'nodeInfos' in jsdata and isinstance(jsdata['nodeInfos'], list):
                node_infos = jsdata['nodeInfos']
    except Exception as e:
        flash(f"错误：无法获取节点列表 - {e}", 'error')
        
    return render_template("device/devlist.html", node_infos=node_infos)

