from flask import render_template, redirect, request, url_for, flash, session
from flask_login import current_user, login_user, logout_user
from apps.config import Config
from apps.meshapi import MeshAPI
from apps.device import blueprint
from apps.device.forms import DeviceStatusForm, CompanyForm, freq_dict
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

@blueprint.route("/manage_companies", methods=['GET', 'POST'])
def manage_companies():
    """
    处理公司数据的添加和编辑操作。
    """
    form = CompanyForm()
    company_to_edit = None # 用于在编辑模式下预填充表单

    # 处理表单提交 (新增或更新)
    if form.validate_on_submit():
        if 'add_company' in request.form:
            # 创建新的公司实例
            new_company = Company(
                com_name=form.com_name.data,
                district=form.district.data,
                street=form.street.data,
                size=form.size.data,
                type=form.type.data,
                address=form.address.data,
                credit_code=form.credit_code.data,
                lon=form.lon.data,
                lat=form.lat.data,
                sys_org_code=form.sys_org_code.data
            )
            try:
                new_company.save()
                flash('公司添加成功！', 'success')
                return redirect(url_for('company_blueprint.companylist')) # 添加后重定向到列表页
            except Exception as e:
                flash(f'添加公司失败: {e}', 'error')

        elif 'update_company' in request.form:
            company_id = request.form.get('company_id_hidden', type=int) # 从隐藏字段获取公司ID
            if company_id:
                company = Company.find_by_id(company_id)
                if company:
                    try:
                        # 更新公司信息
                        company.com_name = form.com_name.data
                        company.district = form.district.data
                        company.street = form.street.data
                        company.size = form.size.data
                        company.type = form.type.data
                        company.address = form.address.data
                        company.credit_code = form.credit_code.data
                        company.lon = form.lon.data
                        company.lat = form.lat.data
                        company.sys_org_code = form.sys_org_code.data

                        company.save() # 保存更新后的公司
                        flash('公司信息更新成功！', 'success')
                        return redirect(url_for('company_blueprint.companylist')) # 更新后重定向到列表页
                    except Exception as e:
                        flash(f'更新公司失败: {e}', 'error')
                else:
                    flash('公司未找到，无法更新。', 'error')
            else:
                flash('未提供公司ID，无法更新。', 'error')
    
    # 处理删除操作 (通常从列表页触发，但也可以在这里处理)
    # 此处删除逻辑保留在 manage 页面，也可以考虑单独的 /delete/<id> 路由
    elif request.method == 'POST' and 'delete_company' in request.form:
        company_id = request.form.get('company_id_to_delete', type=int)
        if company_id:
            company = Company.find_by_id(company_id)
            if company:
                try:
                    company.delete()
                    flash('公司删除成功！', 'success')
                    return redirect(url_for('company_blueprint.companylist')) # 删除后重定向到列表页
                except Exception as e:
                    flash(f'删除公司失败: {e}', 'error')
            else:
                flash('公司未找到，无法删除。', 'error')
        else:
            flash('未提供公司ID，无法删除。', 'error')

    # 对于 GET 请求，或当 POST 请求验证失败时（重新渲染表单）
    if request.method == 'GET':
        if 'edit_id' in request.args:
            edit_id = request.args.get('edit_id', type=int)
            company_to_edit = Company.find_by_id(edit_id)
            if company_to_edit:
                form.process(obj=company_to_edit) # 使用 process(obj=...) 方法填充表单
            else:
                flash('公司未找到。', 'warning')

    return render_template("device/company.html", form=form, company_to_edit=company_to_edit)

# --- 新增的 /list 路由 ---
@blueprint.route("/companylist", methods=['GET'])
def companylist():
    """
    显示公司列表。
    """
    companies = Company.get_list() # 获取所有公司数据
    return render_template("device/company.html", companies=companies)
    
