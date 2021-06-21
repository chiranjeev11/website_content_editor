$(document).ready(function(){


			$('body').on('shown.bs.modal', '.modal', function() {
			  $(this).find('#robots').each(function() {
			    var dropdownParent = $(document.body);
			    if ($(this).parents('.modal.in:first').length !== 0)
			      dropdownParent = $(this).parents('.modal.in:first');
			    $(this).select2({
			      dropdownParent: $('.modal'),
			      width: '100%',
				  placeholder: "Enter robots   eg - index,follow"
			    });
			  });
			});

			$('#robots').change(function(){
				$('#robo').val($(this).val());
			})

			$('.image-preview').hide()


			$('.edit-meta').on('click', editMeta);


			


			$(document).on('change', '#image-input', show_image)

			$(document).on('input', '.recommand', add_recommandation)

			$(document).on('input', '#url-slug', slug_validation)

			$(document).on('click', '.view-image', view_image)








			var image_status = 'view';


			function editMeta(){

				document.querySelector('body').style.opacity = 0.7;
				document.querySelector('.loader').style.display = 'block';

				let page_name = $(this).parent().siblings().first().text();
				



				let checkboxes = document.getElementsByClassName('form-check-input');

				let title_description = document.getElementsByClassName('check');


				


				Array.from(checkboxes).forEach(function(element) {
				element.addEventListener('change', check);
				});

				Array.from(title_description).forEach(function(element) {
				element.addEventListener('input', check);
				});



				$.ajax({
					type:'POST',
					url: "/admin/pages/edit-request",
					success: function(result){
						document.getElementById('page-name').value = result.page_name;
						document.getElementById('url-slug').value = result.url_slug;
						if (result.meta_title!='undefined'){
							document.getElementById('title').value = result.meta_title;
						}
						if (result.meta_description!='undefined'){
							document.getElementById('description').value = result.meta_description;
						}
						if (result.meta_keywords!='undefined'){
							document.getElementById('keywords').value = result.meta_keywords;
						}
						if (result.meta_robots!='undefined'){

							let values = result.meta_robots.split(',');

							$('#robots').select2().val(values).trigger('change');
						}
						if (result.meta_canonical!='undefined'){
							document.getElementById('canonical').value = result.meta_canonical;
						}
						if (result.og_type!='undefined'){
							document.getElementById('type').value = result.og_type;
						}
						if (result.og_title!='undefined'){
							document.getElementById('ogtitle').value = result.og_title;
						}
						if (result.og_description!='undefined'){
							document.getElementById('ogdescription').value = result.og_description;
						}
						
						
						
						document.getElementsByClassName('modal-title')[0].innerHTML = result.page_name;



						if (result.og_image){
							let url = '/static/crop_images/'
							url = url+result.og_image;
							$('.image-preview').attr('src', url);
						}

						document.querySelector('body').style.opacity = 1;
						
						document.querySelector('.loader').style.display = 'none';

						$('#editModal').modal('show');


						let save_button = document.getElementById('submit-form');

						save_button.addEventListener('click', form_submit);

			

						
						
					},
					data: {'data':page_name}

				})
				
			}

			function view_image(){
				$('.image-preview').fadeToggle();
				if (image_status=='view'){
					$('.view-image').text('Hide Image');
					image_status = 'hide';
				}
				else{
					$('.view-image').text('View Image');
					image_status = 'view';
				}
				
			}



			function check(){

					let check1 = document.getElementById("title-checkbox").checked;
					let check2 = document.getElementById("description-checkbox").checked;


					if(check1){
						document.getElementById('ogtitle').value = document.getElementById('title').value;
						document.getElementById('ogtitle').readOnly = true;

					}
					else{
						document.getElementById('ogtitle').readOnly = false;
					}
					if(check2){
						document.getElementById('ogdescription').value = document.getElementById('description').value;
						document.getElementById('ogdescription').readOnly = true;
					}
					else{
						document.getElementById('ogdescription').readOnly = false;
					}
				}


			var slug_validate = true;
			

			function form_submit(){

				if (slug_validate){
					$('.edit-form').submit();
				}

				


			}



			function show_image(event){

				let reader = new  FileReader()

				reader.onload = function(){
					let img = new Image;
					img.onload = function(e){
						if (img.height>700 || img.height<550 || img.width>1350 || img.width<1200){
							$('.ogimage').text(`1280pixels x 627pixels recommanded. Your image dimension is ${img.width} x ${img.height}`);
							$('.ogimage').show();
						}
						else{
							$('.ogimage').hide()
						}
					}
					img.src = reader.result;
					$('#image-bin').attr('value', img.src);
				}

				reader.readAsDataURL(event.target.files[0]);

			}

			function image_recommandation(width, height){
				$('.ogimage').show()
			}

			function add_recommandation(event){

				

				if (event.target.id=='description'){
					if (event.target.value.length>160 || event.target.value.length<50){

						$('.description').show();
					}
					else{
						$('.description').hide();
					}
				}

				if (event.target.id=='ogdescription'){
					if (event.target.value.length>160 || event.target.value.length<50){

						$('.ogdescription').show();
					}
					else{
						$('.ogdescription').hide();
					}
				}

				if (event.target.id=='keywords'){

					let words = event.target.value.split(',').length;

					if (words>10){

						$('.keywords').show();
					}
					else{
						$('.keywords').hide();
					}
				}


			}


			function slug_validation(event){

				if (/(^\/$|^(\/[a-z-]+)+\/?$)/.test($('#url-slug').val()) == false){
					$('.url-slug').show();
					slug_validate = false;
				}
				else{
					$('.url-slug').hide();
					slug_validate = true;
				}

			}


			

		})
