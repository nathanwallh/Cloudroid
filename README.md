# Cloudroid

Project for the RBD lab, Haifa University.
<!DOCTYPE html>
<html lang = "en">
   
	<head>
		<meta charset = "utf-8">
		<meta http-equiv = "X-UA-Compatible" content = "IE = edge">
		<meta name = "viewport" content = "width = device-width, initial-scale = 1">

		<title> Cloudroid </title>

		<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css" integrity="sha384-BVYiiSIFeK1dGmJRAkycuHAHRg32OmUcww7on3RYdg4Va+PmSTsz/K68vbdEjh4u" crossorigin="anonymous">

		<!-- Optional theme -->
		<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap-theme.min.css" integrity="sha384-rHyoN1iRsVXV4nD0JutlnGaslCJuC7uwjduW9SVrLvRYooPp2bWYgmgJQIXwl/Sp" crossorigin="anonymous">

		<!-- Latest compiled and minified JavaScript -->
		<script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/js/bootstrap.min.js" integrity="sha384-Tc5IQib027qvyjSMfHjOMaLkfuWVxZxUPnCJA7l2mCWNIpG9mGCD8wGNIcPD7Txa" crossorigin="anonymous"></script>
		
		<script src="https://ajax.googleapis.com/ajax/libs/jquery/1.11.0/jquery.min.js"></script>
		
		<script src="https://cdnjs.cloudflare.com/ajax/libs/jssor-slider/22.1.8/jssor.slider.min.js" type="text/javascript"></script>

		<script type="text/javascript">
			jQuery(document).ready(function ($) {

				var jssor_1_SlideshowTransitions = [
				  {$Duration:1200,$Zoom:1,$Easing:{$Zoom:$Jease$.$InCubic,$Opacity:$Jease$.$OutQuad},$Opacity:2},
				  {$Duration:1000,$Zoom:11,$SlideOut:true,$Easing:{$Zoom:$Jease$.$InExpo,$Opacity:$Jease$.$Linear},$Opacity:2},
				  {$Duration:1200,$Zoom:1,$Rotate:1,$During:{$Zoom:[0.2,0.8],$Rotate:[0.2,0.8]},$Easing:{$Zoom:$Jease$.$Swing,$Opacity:$Jease$.$Linear,$Rotate:$Jease$.$Swing},$Opacity:2,$Round:{$Rotate:0.5}},
				  {$Duration:1000,$Zoom:11,$Rotate:1,$SlideOut:true,$Easing:{$Zoom:$Jease$.$InExpo,$Opacity:$Jease$.$Linear,$Rotate:$Jease$.$InExpo},$Opacity:2,$Round:{$Rotate:0.8}},
				  {$Duration:1200,x:0.5,$Cols:2,$Zoom:1,$Assembly:2049,$ChessMode:{$Column:15},$Easing:{$Left:$Jease$.$InCubic,$Zoom:$Jease$.$InCubic,$Opacity:$Jease$.$Linear},$Opacity:2},
				  {$Duration:1200,x:4,$Cols:2,$Zoom:11,$SlideOut:true,$Assembly:2049,$ChessMode:{$Column:15},$Easing:{$Left:$Jease$.$InExpo,$Zoom:$Jease$.$InExpo,$Opacity:$Jease$.$Linear},$Opacity:2},
				  {$Duration:1200,x:0.6,$Zoom:1,$Rotate:1,$During:{$Left:[0.2,0.8],$Zoom:[0.2,0.8],$Rotate:[0.2,0.8]},$Easing:{$Left:$Jease$.$Swing,$Zoom:$Jease$.$Swing,$Opacity:$Jease$.$Linear,$Rotate:$Jease$.$Swing},$Opacity:2,$Round:{$Rotate:0.5}},
				  {$Duration:1000,x:-4,$Zoom:11,$Rotate:1,$SlideOut:true,$Easing:{$Left:$Jease$.$InExpo,$Zoom:$Jease$.$InExpo,$Opacity:$Jease$.$Linear,$Rotate:$Jease$.$InExpo},$Opacity:2,$Round:{$Rotate:0.8}},
				  {$Duration:1200,x:-0.6,$Zoom:1,$Rotate:1,$During:{$Left:[0.2,0.8],$Zoom:[0.2,0.8],$Rotate:[0.2,0.8]},$Easing:{$Left:$Jease$.$Swing,$Zoom:$Jease$.$Swing,$Opacity:$Jease$.$Linear,$Rotate:$Jease$.$Swing},$Opacity:2,$Round:{$Rotate:0.5}},
				  {$Duration:1000,x:4,$Zoom:11,$Rotate:1,$SlideOut:true,$Easing:{$Left:$Jease$.$InExpo,$Zoom:$Jease$.$InExpo,$Opacity:$Jease$.$Linear,$Rotate:$Jease$.$InExpo},$Opacity:2,$Round:{$Rotate:0.8}},
				  {$Duration:1200,x:0.5,y:0.3,$Cols:2,$Zoom:1,$Rotate:1,$Assembly:2049,$ChessMode:{$Column:15},$Easing:{$Left:$Jease$.$InCubic,$Top:$Jease$.$InCubic,$Zoom:$Jease$.$InCubic,$Opacity:$Jease$.$OutQuad,$Rotate:$Jease$.$InCubic},$Opacity:2,$Round:{$Rotate:0.7}},
				  {$Duration:1000,x:0.5,y:0.3,$Cols:2,$Zoom:1,$Rotate:1,$SlideOut:true,$Assembly:2049,$ChessMode:{$Column:15},$Easing:{$Left:$Jease$.$InExpo,$Top:$Jease$.$InExpo,$Zoom:$Jease$.$InExpo,$Opacity:$Jease$.$Linear,$Rotate:$Jease$.$InExpo},$Opacity:2,$Round:{$Rotate:0.7}},
				  {$Duration:1200,x:-4,y:2,$Rows:2,$Zoom:11,$Rotate:1,$Assembly:2049,$ChessMode:{$Row:28},$Easing:{$Left:$Jease$.$InCubic,$Top:$Jease$.$InCubic,$Zoom:$Jease$.$InCubic,$Opacity:$Jease$.$OutQuad,$Rotate:$Jease$.$InCubic},$Opacity:2,$Round:{$Rotate:0.7}},
				  {$Duration:1200,x:1,y:2,$Cols:2,$Zoom:11,$Rotate:1,$Assembly:2049,$ChessMode:{$Column:19},$Easing:{$Left:$Jease$.$InCubic,$Top:$Jease$.$InCubic,$Zoom:$Jease$.$InCubic,$Opacity:$Jease$.$OutQuad,$Rotate:$Jease$.$InCubic},$Opacity:2,$Round:{$Rotate:0.8}}
				];

				var jssor_1_options = {
				  $AutoPlay: true,
				  $SlideshowOptions: {
					$Class: $JssorSlideshowRunner$,
					$Transitions: jssor_1_SlideshowTransitions,
					$TransitionsOrder: 1
				  },
				  $ArrowNavigatorOptions: {
					$Class: $JssorArrowNavigator$
				  },
				  $ThumbnailNavigatorOptions: {
					$Class: $JssorThumbnailNavigator$,
					$Rows: 2,
					$Cols: 6,
					$SpacingX: 14,
					$SpacingY: 12,
					$Orientation: 2,
					$Align: 156
				  }
				};

				var jssor_1_slider = new $JssorSlider$("jssor_1", jssor_1_options);

				/*responsive code begin*/
				/*you can remove responsive code if you don't want the slider scales while window resizing*/
				function ScaleSlider() {
					var refSize = jssor_1_slider.$Elmt.parentNode.clientWidth;
					if (refSize) {
						refSize = Math.min(refSize, 960);
						refSize = Math.max(refSize, 300);
						jssor_1_slider.$ScaleWidth(refSize);
					}
					else {
						window.setTimeout(ScaleSlider, 30);
					}
				}
				ScaleSlider();
				$(window).bind("load", ScaleSlider);
				$(window).bind("resize", ScaleSlider);
				$(window).bind("orientationchange", ScaleSlider);
				/*responsive code end*/
			});
    </script>
		<style>
			/* jssor slider arrow navigator skin 05 css */
			/*
			.jssora05l                  (normal)
			.jssora05r                  (normal)
			.jssora05l:hover            (normal mouseover)
			.jssora05r:hover            (normal mouseover)
			.jssora05l.jssora05ldn      (mousedown)
			.jssora05r.jssora05rdn      (mousedown)
			.jssora05l.jssora05lds      (disabled)
			.jssora05r.jssora05rds      (disabled)
			*/
			.jssora05l, .jssora05r {
				display: block;
				position: absolute;
				/* size of arrow element */
				width: 40px;
				height: 40px;
				cursor: pointer;
				background: url('img/a17.png') no-repeat;
				overflow: hidden;
			}
			.jssora05l { background-position: -10px -40px; }
			.jssora05r { background-position: -70px -40px; }
			.jssora05l:hover { background-position: -130px -40px; }
			.jssora05r:hover { background-position: -190px -40px; }
			.jssora05l.jssora05ldn { background-position: -250px -40px; }
			.jssora05r.jssora05rdn { background-position: -310px -40px; }
			.jssora05l.jssora05lds { background-position: -10px -40px; opacity: .3; pointer-events: none; }
			.jssora05r.jssora05rds { background-position: -70px -40px; opacity: .3; pointer-events: none; }
			/* jssor slider thumbnail navigator skin 01 css *//*.jssort01-99-66 .p            (normal).jssort01-99-66 .p:hover      (normal mouseover).jssort01-99-66 .p.pav        (active).jssort01-99-66 .p.pdn        (mousedown)*/.jssort01-99-66 .p {    position: absolute;    top: 0;    left: 0;    width: 99px;    height: 66px;}.jssort01-99-66 .t {    position: absolute;    top: 0;    left: 0;    width: 100%;    height: 100%;    border: none;}.jssort01-99-66 .w {    position: absolute;    top: 0px;    left: 0px;    width: 100%;    height: 100%;}.jssort01-99-66 .c {    position: absolute;    top: 0px;    left: 0px;    width: 95px;    height: 62px;    border: #000 2px solid;    box-sizing: content-box;    background: url('img/t01.png') -800px -800px no-repeat;    _background: none;}.jssort01-99-66 .pav .c {    top: 2px;    _top: 0px;    left: 2px;    _left: 0px;    width: 95px;    height: 62px;    border: #000 0px solid;    _border: #fff 2px solid;    background-position: 50% 50%;}.jssort01-99-66 .p:hover .c {    top: 0px;    left: 0px;    width: 97px;    height: 64px;    border: #fff 1px solid;    background-position: 50% 50%;}.jssort01-99-66 .p.pdn .c {    background-position: 50% 50%;    width: 95px;    height: 62px;    border: #000 2px solid;}* html .jssort01-99-66 .c, * html .jssort01-99-66 .pdn .c, * html .jssort01-99-66 .pav .c {    /* ie quirks mode adjust */    width /**/: 99px;    height /**/: 66px;}
		</style>
	</head>
   
	<body class ="well">
		<div class = "container">
			<div class="well">
				<h1 class="text-primary"> <b> Cloudroid - Cloud storage on a network of Odroid devices  </b> </h1>      
				
			</div>
			
			<div class="panel panel-primary">
				<div class="panel-heading">
					<h3 class="panel-title">Description</h3>
				</div>
				<h4>
					<div class="panel-body ">
						<p class="text-success">
							A basic cloud storage mechanism based on the FTP protocol, ideal for file sharing between multiple peers.
							It consists of FTP servers connected together remotely, where each server has its own copy of shared directory.
							FTP commands that are sent to one server, are broadcasted to every server on the network, so that the network operates as one unit.
						</p>
					</div>
				</h4>
			</div>
			
			<div class="panel panel-primary">
				<div class="panel-heading">
					<h3 class="panel-title">Protocol overview</h3>
				</div>
				<h4>
					<div class="panel-body ">
						<p class="text-success">
							A "Cloudroid" server consists of 2 processes running together:
							</br>1. FTP server - Taken from the pyftpdlib library.
							</br>2. Proxy server - Implemented by us.
							The FTP server works in the background. The proxy server, however, is the client's gateway to the network. It accepts clients connections, broadcasts
							traffic to the network, and multiplexes replies to the client.
							When a client connection is made, the proxy server connects to all FTP servers on the network. These servers are listed in the file <b> 'PEERS.txt' </b>.
							</br>The network can be diagrammed as follows:
							
							<img src="img/diagram.png" class="img-responsive" alt="Cinque Terre">
							
							It should be noted that connections between proxy servers and FTP servers(or equivalently: between FTP clients and FTP servers), actually consist of 2 different connections:
							</br>1. Control connection.
							</br>2. Data connection.
							</br>
							This is a inherent part of the FTP protocol that the proxy server must take care of.</br>
							The control connection is used to send FTP commands and recieve return codes, while the data connection is used to send and recieve data (e.g: when sending files).
							Data connections are opened for client requests and they are disposable. For each session, many data connections might be opened and closed, but the control connection remain.
							The proxy server deals with it by creating data connection with all FTP servers in the network except of the local FTP server. The data connection of the local FTP server is redirected back to the client.
							Therefore, when the client exchanges data with the network, he actually exchanges it with one server only. When he finishes, the proxy server uses it's own data connections with other servers to broadcast
							the data to the network.

							Another important aspect of the protocol is a consistency check procedure that runs every time a new session with client begins.
							This procedure ensures that the files in the shared directory of one server will be the same files in the shared directory of other servers in the network.
							To decide if a server is consistent or not, a special parameter named CONSISTENCY_THRESHOLD is defined. It is a number between 0 to 1, that gives the percentile of servers allowed to differ
							from the server under check.
						</p>
					</div>
				</h4>
			</div>
			
			
			<h3 class="text-primary"><b> Images </b> </h3>
			<div id="jssor_1" style="position:relative;margin:0 auto;top:0px;left:0px;width:960px;height:480px;overflow:hidden;visibility:hidden;background-color:#24262e;">
				<!-- Loading Screen -->
				<div data-u="loading" style="position:absolute;top:0px;left:0px;background-color:rgba(0,0,0,0.7);">
					<div style="filter: alpha(opacity=70); opacity: 0.7; position: absolute; display: block; top: 0px; left: 0px; width: 100%; height: 100%;"></div>
					<div style="position:absolute;display:block;background:url('img/loading.gif') no-repeat center center;top:0px;left:0px;width:100%;height:100%;"></div>
				</div>
				<div data-u="slides" style="cursor:default;position:relative;top:0px;left:240px;width:720px;height:480px;overflow:hidden;">
					<div>
						<img data-u="image" src="img/demo1.png" />
					</div>
					<a data-u="any" href="http://www.jssor.com" style="display:none">Image Gallery with Vertical Thumbnail</a>
					<div>
						<img data-u="image" src="img/demo2.png" />
					</div>

				</div>
				<!-- Thumbnail Navigator -->
				<div data-u="thumbnavigator" class="jssort01-99-66" style="position:absolute;left:0px;top:0px;width:240px;height:480px;" data-autocenter="2">
					<!-- Thumbnail Item Skin Begin -->
					<div data-u="slides" style="cursor: default;">
						<div data-u="prototype" class="p">
							<div class="w">
								<div data-u="thumbnailtemplate" class="t"></div>
							</div>
							<div class="c"></div>
						</div>
					</div>
					<!-- Thumbnail Item Skin End -->
				</div>
				<!-- Arrow Navigator -->
				<span data-u="arrowleft" class="jssora05l" style="top:0px;left:248px;width:40px;height:40px;" data-autocenter="2"></span>
				<span data-u="arrowright" class="jssora05r" style="top:0px;right:8px;width:40px;height:40px;" data-autocenter="2"></span>
			</div>
			<!-- #endregion Jssor Slider End -->	

			
			
			</br></br></br>
			
			<h3 class="text-primary"><b> Video </b> </h3>
			<!-- 16:9 aspect ratio -->
			<div class="embed-responsive embed-responsive-16by9">
				<iframe class="embed-responsive-item" src="https://www.youtube.com/embed/VlxFEtmz39s"></iframe>
			</div>
			</br></br></br>
			
			<h3 class="text-primary"><b> Sources </b> </h3>
			<div class="panel-grid-cell" >
					<a class="btn btn-info" href="https://github.com/nathanwallh/Cloudroid/archive/master.zip" role="button" class="col-md-3"> Cloudroid.zip</a>
				
					&nbsp&nbsp&nbsp
					<a class="btn btn-info" href="https://github.com/nathanwallh/Cloudroid" role="button" class="col-md-3"> Github</a>
			</div>
			</br>
			<h3 class="text-primary"><b> Developers </b> </h3>
			<div class="text-success">
				Nathan Wallheimer - nathanwallh@gmail.com</br>
				Efraimov Oren - Orenef11@gmail.com</br>
			</div>
			
			
			
		</div>

	</body>
</html>
