from flask import render_template, redirect, request, url_for, flash, session
from flask_login import current_user, login_user, logout_user
from flask_wtf.csrf import generate_csrf
from apps.config import Config
from apps.meshapi import MeshAPI
from apps.company import blueprint
from apps.company.forms import CompanyForm
from apps.models import Company

@blueprint.route("/add_company", methods=['POST'])
def add_company():
    """
    处理从模态框提交的新公司数据。
    """
    form = CompanyForm()
    if form.validate_on_submit():
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
            ret, msg =  new_company.save()
            if ret:
                flash(f'公司 {form.com_name.data} 添加成功！', 'success')
            else:
                flash(f'公司 {form.com_name.data} 添加失败: {msg}', 'error')
            return redirect(url_for('company_blueprint.companylist'))
        except Exception as e:
            flash(f'添加公司失败: {e}', 'error')
    else:
        for field, errors in form.errors.items():
            for error in errors:
                flash(f'字段 {getattr(form, field).label.text} 错误: {error}', 'error')
    
    return redirect(url_for('company_blueprint.companylist'))


@blueprint.route("/delete_company", methods=['POST'])
def delete_company():
    """
    处理删除公司请求。
    """
    if request.method == 'POST' and 'delete_company' in request.form:
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

@blueprint.route("/manage_companies", methods=['GET', 'POST'])
def manage_companies():
    """
    处理公司数据的添加和编辑操作。
    """
    form = CompanyForm()
    company_to_edit = None # 用于在编辑模式下预填充表单

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
                ret, msg = new_company.save()
                if ret:
                    flash('公司添加成功！', 'success')
                else:
                    flash(f'公司添加失败: {msg}', 'error')
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

                        ret, msg = new_company.save()
                        if ret:
                            flash('公司更新成功！', 'success')
                        else:
                            flash(f'公司更新失败: {msg}', 'error')
                        return redirect(url_for('company_blueprint.companylist')) # 更新后重定向到列表页
                    except Exception as e:
                        flash(f'更新公司失败: {e}', 'error')
                else:
                    flash('公司未找到，无法更新。', 'error')
            else:
                flash('未提供公司ID，无法更新。', 'error')
    

    # 对于 GET 请求，或当 POST 请求验证失败时（重新渲染表单）
    if request.method == 'GET':
        if 'edit_id' in request.args:
            edit_id = request.args.get('edit_id', type=int)
            company_to_edit = Company.find_by_id(edit_id)
            if company_to_edit:
                form.process(obj=company_to_edit) # 使用 process(obj=...) 方法填充表单
            else:
                flash('公司未找到。', 'warning')

    return render_template("company/company.html", form=form, company_to_edit=company_to_edit)


@blueprint.route("/companylist", methods=['GET'])
def companylist():
    """
    显示公司列表。
    """
    companies = Company.get_list()
    # 显式地生成 CSRF token 并传递给模板
    csrf_token = generate_csrf()
    return render_template(
        "company/company.html", 
        companies=companies, 
        csrf_token=csrf_token
    )