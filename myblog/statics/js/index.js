$(function(){
	// 计算图片数量添加对应的小圆点
	var $li = $(".ulm li");
			var len = $li.length;
			$li.not(":first").css({left:400});
			$li.each(function(index){
				// 判断当前图片是哪一张修改对应圆点的属性样式
				var $sli=$("<li>");
				if(index == 0){
					$sli.addClass('active');  
				}
				$sli.appendTo(".point");
			})
			// 点击对应的圆点所能触发的事件和动画
			var nowli=0;
			var nextli=0;
			var $point=$(".point li");
			$point.click(function(){
				nextli=$(this).index();
				move()
				$(this).addClass("active").siblings().removeClass("active");

			})
			// 点击左边箭头的事件
			$(".rightclick").click(function(){
				nextli++;
				move();
				$point.eq(nextli).addClass("active").siblings().removeClass("active");

			})
			// 点击右边箭头的事件
			$(".leftclick").click(function(){
				nextli--;
				move();
				$point.eq(nextli).addClass("active").siblings().removeClass("active");

			})
			// 鼠标移入移除事件
			$(".picvideo").mouseenter(function(){
				clearInterval(timer);
			})

			$(".picvideo").mouseleave(function(){
				timer = setInterval(autoplay,4000);
			})

			timer = setInterval(autoplay,4000);



			// 自动播放动画
			function autoplay(){
				nextli++;
				move();
				$point.eq(nextli).addClass("active").siblings().removeClass("active");
			}
			// 图片移动动画判断函数
			function move(){
				if(nextli>len-1){
					nextli=0;
					$li.eq(nextli).css({left:400});
					$li.eq(nowli).stop().animate({left:-400});
					$li.eq(nextli).stop().animate({left:0});
					nowli=nextli;
					return;}
				if(nextli<0){
					nextli=len-1;
					nowli=0;
					$li.eq(nextli).css({left:-400});
					$li.eq(nowli).stop().animate({left:400});
					$li.eq(nextli).stop().animate({left:0});
					nowli=nextli;
					return;
				}
				if(nextli>nowli){
					$li.eq(nextli).css({left:400});
					$li.eq(nowli).stop().animate({left:-400});
					$li.eq(nextli).stop().animate({left:0});
					nowli=nextli;
					return
				}
				else if(nextli<nowli){
					$li.eq(nextli).css({left:-400});
					$li.eq(nowli).stop().animate({left:400});
					$li.eq(nextli).stop().animate({left:0});
					nowli=nextli;
					return;
				}
				else{
					nextli==nowli;
					return;
				}
			}





})