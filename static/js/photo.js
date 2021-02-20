/**
 * Created by gaowei on 2021/01/25
 */

$(document).ready(function () {
    let photo = new Photo();
    photo.init();
    photo.table();
});
let Photo = function () {
};
Photo.prototype = {
    init: function () {
           $('#bt_submit').click(function () {
            console.log("sssss")
            let photo = $('#photo').val();
            let photo_name = $('#photo_name').val();
            let description = $('#description').val();

            if ($.trim(user_mobile) === '') {
                Alert.prototype.alertWarning("陛下后台账号不能为空");
                return;
            } else {
                param = {
                    'photo': photo,
                    'photo_name': photo_name,
                    'description': description,
                };
                Alert.prototype.alertLoading();
                $.ajax({
                    type: 'post',
                    url: '/photo_upload/',
                    // dataType: 'json',
                    data: param,
                    success: function (res) {
//                        $('#task_check_result').val(res);
//                        $('#service_list_table').bootstrapTable('refresh');
                        Alert.prototype.alertInfo(res)
                    }
                });
            }
        });
           $('#bt_search').click(function () {
                    let user_mobile = $('#user_mobile').val();
                    let task_id = $('#task_id').val();
                    let env = $('#env').val();

                    if ($.trim(user_mobile) === '') {
                        Alert.prototype.alertWarning("陛下后台账号不能为空");
                        return;
                    } else if ($.trim(task_id) === '') {
                        Alert.prototype.alertWarning("陛下任务编号都不能为空");
                        return;
                    } else {
                        param = {
                            'user_mobile': user_mobile,
                            'task_id': task_id,
                            'env': env,
                        };
                        Alert.prototype.alertLoading();
                        $.ajax({
                            type: 'post',
                            url: '/tools/taskcheck',
                            // dataType: 'json',
                            data: param,
                            success: function (res) {
                                $('#task_check_result').val(res);
                                $('#service_list_table').bootstrapTable('refresh');
                                Alert.prototype.alertInfo(res)
                            }
                        });
                    }
                });


       },
    table: function () {
        $('#photo_list_table').bootstrapTable({
            url: '/photo_index/',
            method: 'get',
            // data: res,
            search: true,
            // showColumns: true,
            // checkboxHeader: true,
            sortStable: true,
            striped: true,
            pagination: true,
            onlyInfoPagination: false,
            sortOrder: 'desc',
            showRefresh: true,
            // pageSize: 10, //控制每页显示个数
            toolbar: '#tableToolbar',
            columns: [
                {
                    field: 'photo_id',
                    title: '图片id',
                    // width: '50%',
                },
                {
                    field: 'photo_name',
                    title: '后台账号'
                },
                {
                    field: 'photo',
                    title: '执行环境'
                },
                {
                    field: 'description',
                    title: '返回信息'
                },
                {
                    field: 'click',
                    title: '执行时间'
                },
                {
                    field: 'category_photo_id',
                    title: '工具名称'
                }
            ]
        });
    },
};