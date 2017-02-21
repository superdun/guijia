
function __initHtmlEditorUploader__(uploader,editor) {

	if (!uploader) {
		return false;
	}

	var uploaderNoty = [];
	var url = '/../admin/upload'
	var findNoty = function (file) {
		var i,
		item;
		for (i in uploaderNoty) {
			item = uploaderNoty[i];
			if (file.originalName == item.file) {
				return item.noty;
			}
		}
		return false;
	}

	uploader.fileupload({
		url : url,
		dataType : 'json',
		send : function (e, data) {
			var files = data.files,
			i = 0,
			file;
			for (i in files) {
				file = files[i];
				uploaderNoty.push({
					file : file.name,
					noty : noty({
						text : 'Uploading file ' + files[i].name
					})
				});
			}
			//console.log(files);
		},
		done : function (e, data) {
			//var editor = uploader.data('eva-ui');
			var file = data.result;
			console.log(data);
			var notyHandle = findNoty(file);
			if (notyHandle) {
				notyHandle.setText(file.originalName + ' uploaded.').setType('success');
				setTimeout(function () {
					notyHandle.close();
				}, 2000);
			}
			if (file.isImage > 0) {
				editor.insertHtml('<img src="' + file.localUrl + '" alt="' + file.title + '" />');
			} else {
				editor.insertHtml('<a href="' + file.localUrl + '">' + file.fileName + '</a>');
			}
			//console.log(data);
		},
		progressall : function (e, data) {
			//console.log(data);
		}
	});

}

CKEDITOR.plugins.add('uploader', {
	//lang:['zh-cn','en'],
	init : function (editor) {
		var command = new CKEDITOR.command(editor, {
				exec : function (editor) {
					//alert(editor.document.getBody().getHtml());
				}
			});
		var b = editor.addCommand('uploader_cmd', command),
		randomId = parseInt(1000 * Math.random());
		editor.ui.addButton('UploaderBtn', {
			id: "uploaderBtn",
			name : "uploaderBtn",
			label : "插入图片",
			command : 'uploader_cmd',
			toolbar : 'insert',
			className : 'uploadFile' + randomId,
			icon : this.path + 'images/uploader.png'
		});

		editor.on("instanceReady", function (evt) {

			var cn = "." + editor.ui.items["UploaderBtn"].className;
			$(cn).parent().css("position", "relative");
			var fileUploader = $('<input type="file" multiple="" class="editor-upload-handle" ' +
					'data-connect-editor=".editor-content" style="position: absolute;width:32px;height:32px;opacity: 0;-ms-filter: \'alpha(opacity=0)\';direction: ltr;cursor: pointer;">');
			$(cn).after(fileUploader);
			
			__initHtmlEditorUploader__(fileUploader,editor);
		});

	}
});
