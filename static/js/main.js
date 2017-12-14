/*
	Metronic by TEMPLATE STOCK
	templatestock.co @templatestock
	Released for free under the Creative Commons Attribution 3.0 license (templated.co/license)
*/


(function($) {
	"use strict";
	
		/*====================================
		 Bootstrap Fix For WinPhone 8 And IE10
		======================================*/
		
		if (navigator.userAgent.match(/IEMobile\/10\.0/)) {
			var msViewportStyle = document.createElement("style");
			msViewportStyle.appendChild(
				document.createTextNode(
					"@-ms-viewport{width:auto!important}"
				)
			);
			document.getElementsByTagName("head")[0].
				appendChild(msViewportStyle);
		}	
		
		
		/*====================================
					Android stock browser
		======================================*/
		
		$(function () {
		  var nua = navigator.userAgent
		  var isAndroid = (nua.indexOf('Mozilla/5.0') > -1 && nua.indexOf('Android ') > -1 && nua.indexOf('AppleWebKit') > -1 && nua.indexOf('Chrome') === -1)
		  if (isAndroid) {
			$('select.form-control').removeClass('form-control').css('width', '100%')
		  }
		})	



		/*====================================
					Preloader
		======================================*/

		$(window).load(function() {
		
			var preloaderDelay = 350,
				preloaderFadeOutTime = 800;
	
			function hidePreloader() {
				var loadingAnimation = $('#loading-animation'),
					preloader = $('#preloader');
	
				loadingAnimation.fadeOut();
				preloader.delay(preloaderDelay).fadeOut(preloaderFadeOutTime);
			}
	
			hidePreloader();
	
		});
		
		
		
		/*====================================
					Background
		======================================*/
		
		//Image Background 
		$(".image-background").backstretch("../static/images/image-bg.jpg");
		
		
		
		//Parallax Background 
		if($('body').hasClass('parallax-background')) {
					
		$.parallaxify({
			positionProperty: 'transform',
			responsive: true,
			motionType: 'natural',
			mouseMotionType: 'performance',
			motionAngleX: 70,
			motionAngleY: 70,
			alphaFilter: 0.5,
			adjustBasePosition: true,
			alphaPosition: 0.025,
		});
	    } 
		
		//Particle Background 
		$(".particle-background").backstretch("../../assets/images/bg/particle-bg.jpg");
		
		$('.particles').particleground({
		dotColor: '#5cbdaa',
		lineColor: '#5cbdaa',
		parallax: false,
		});
		
		
		
		//Snowdrops Background 
		$(".snowdrops-background").backstretch("../../assets/images/bg/snowdrops-bg.jpg");
				
		//HTML5 Video Background 
		$(".video-background").backstretch("../../assets/video/Storm_darck.jpg");
		
		//Player 
		$(".player").each(function() {
		$(".player").mb_YTPlayer();
		});

		
		
		/*====================================
					Clock Countdown
		======================================*/

		$('#clock-countdown').countdown('2018/12/30 12:00:00').on('update.countdown', function(event) {
			var $this = $(this).html(event.strftime(''
				+ '<div class="counter-container"><div class="counter-box first"><div class="number">%-D</div><span>Day%!d</span></div>'
				+ '<div class="counter-box"><div class="number">%H</div><span>Hours</span></div>'
				+ '<div class="counter-box"><div class="number">%M</div><span>Minutes</span></div>'
				+ '<div class="counter-box last"><div class="number">%S</div><span>Seconds</span></div></div>'
			));
		});
		
		
		
		/*====================================
					Flexslider
		======================================*/

		$('.flexslider').flexslider({
			animation: "fade",
			animationLoop: true,
			slideshowSpeed: 7000,
			animationSpeed: 600,			
			controlNav: false,
			directionNav: false,			
			keyboard: false,			
			start: function(slider){
			$('body').removeClass('loading');
			}
		});


		
		/*====================================
					Flexslider
		======================================*/

		$(document).ready(function() {
		 
		  $("#owl-demo").owlCarousel({
		 
			  autoPlay: 3000, //Set AutoPlay to 3 seconds
		 
			  items : 4,
			  itemsDesktop : [1199,3],
			  itemsDesktopSmall : [979,3]
		 
		  });
		 
		});

		/*====================================
					Nice Scroll
		======================================*/
			
		$("html").niceScroll({
			cursorcolor: '#ccc',
			cursoropacitymin: '0',
			cursoropacitymax: '1',
			cursorwidth: '3px',
			zindex: 10000,
			horizrailenabled: false,
		});

				
			
		/*====================================
					Animated.css
		======================================*/

		$('.animated').appear(function() {
			var element = $(this),
				animation = element.data('animation'),
				animationDelay = element.data('animation-delay');
				if ( animationDelay ) {
	
					setTimeout(function(){
						element.addClass( animation + " visible");
					}, animationDelay);
	
				} else {
					element.addClass( animation + " visible");
				}
		});


			


		/*====================================
					Contact Form
		======================================*/
		
		function initContactForm() {

			var scrollElement = $('html,body'),
				contactForm = $('.contact-form'),
				form_msg_timeout;

			contactForm.on( 'submit', function() {

				var requiredFields = $(this).find('.required'),
					formData = contactForm.serialize(),
					formAction = $(this).attr('action'),
					formSubmitMessage = $('.response-message');

				requiredFields.each(function() {

					if( $(this).val() == "" ) {

						$(this).addClass('input-error');

					} else {

						$(this).removeClass('input-error');
					}

				});

				function validateEmail(email) { 
					var exp = /^(([^<>()[\]\\.,;:\s@\"]+(\.[^<>()[\]\\.,;:\s@\"]+)*)|(\".+\"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
					return exp.test(email);
				}

				var emailField = $('.contact-form-email');

				if( !validateEmail(emailField.val()) ) {

					emailField.addClass("input-error");

				}

				if ($(".contact-form :input").hasClass("input-error")) {
					return false;
				} else {
				
					clearTimeout(form_msg_timeout);
					
					$.post(formAction, formData, function(data) {
						formSubmitMessage.text(data);

						requiredFields.val("");

						form_msg_timeout = setTimeout(function() {
							formSubmitMessage.slideUp();
						}, 5000);
					});

				}

				return false;

			});

		}
		initContactForm();
			


})(jQuery);

$( document ).ready(function(){
	$("#searchbtn").click(function(){

		var query_string = {
	        "search": $("#do-search").val(),
	        "agency": $("#agency-filter option:selected").attr("value"),
	        "content_type": $("#content-type-filter option:selected").attr("value"),
	        "year": $("#pub-year-filter option:selected").attr("value")
	    }
	    query_string = JSON.stringify(query_string)
	    
	    var xhr = new XMLHttpRequest()
	    xhr.open("POST","http://dsg1.crc.nd.edu:5020/query",true)  

	    xhr.onload = function(e){
	        console.log(xhr.responseText)
	        var law_info = JSON.parse(xhr.responseText)
	        buildTable(law_info)

	    }
	    xhr.onerror = function(e){
	        console.error(xhr.statusText);
	    }
	    xhr.send(query_string)

	    /*
		
		$("#results").find("#best-tr").click(function(){
				$("#results").html(
					'<h5> Articles </h5>'+
                    '<ol><li>Purpose of this Order </li><li>Curriculum and teaching hours in primary and secondary schools </li>li>Curriculum and teaching hours in specialized schools </li>'+
                        '<li>Language of instruction in the first cycle of primary education</li><li>Language of instruction in the second cycle of primary education </li>'+
                        '<li>Language of secondary schools </li><li>Language of specialized schools </li><li>Repealing provision </li><li>Commencement</li></ol>'+
				'<table class="result-talbe">'+
						'<tr>'+
                            '<th>Repeals</th>'+
                        '</tr>'+
                        '<tr>'+
                            '<td>N° 002/2016 OF 08/01/2016 DETERMINING THE RESPONSIBILITIES OF SCHOOL MANAGEMENT BOARD MEMBERS</td>'+
                        '</tr>'+
                        '<tr>'+
                            '<th>Reference</th>'+
                        '</tr>'+
                        '<tr>'+
                            '<td>003/2016 OF 08/01/2016 DETERMINING GENERAL RULES GOVERNING NURSERY, PRIMARY AND SECONDARY SCHOOLS AND FUNCTIONING OF SCHOOL GENERAL ASSEMBLY AND ITS SUBSIDIARY ORGANS</td>'+
                        '</tr>'+
                    '</table>'
			)
		})*/
	})

	function buildTable(law_info){
		$("#results").html('')
		$.each( law_info, function( key, value ) {
		  $("#results").append(
				'<table class="result-talbe" date_num="'+key+'">'+
                        '<tr class="pointer-tr law_name"><th>'+
                            'Law Name: '+ value['law_name']+
                        '</th></tr>'+
                        '<tr><td>'+
                        	'Content Type: '+ value['content_type_tag']+
                        '</td></tr><tr><td>'+
                        	'Publication Year: '+ value['pub_year']+
                        '</td></tr><tr><td>'+
                        	'Agency: '+ value['agency_tag']+
                        '</td></tr>'+
                        '<tr><td>'+
                        	'First Article: '+ 
                        '</td></tr>'+
                        '<tr><td>'+
                        	value['article_one_str']+
                        '</td></tr>'+
                    '</table>'
			)
		});
	}


})
