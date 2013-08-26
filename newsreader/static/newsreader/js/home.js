/*
-------------------------
Global variables
-------------------------
*/
var layoutmanager;
var htmlgenerator;
var fetch_lock = false;
var email_lock = false;

/*
-------------------------
Feed related functions
-------------------------
*/
function fetch_article(){
	if(fetch_lock) return; //If fetch_article has been locked, then return

	fetch_lock = true;
	$("#scroll-detect").css("visibility", "visible");
	$("#scroll-detect > div").css("display", "block");
	$("#scroll-detect > span").css("display", "none");
	
	Dajaxice.feeds.get_article(function(data){
		if(data['success'] && data['article'] != null){
			//If article was retrieved, then add it to the layout
			layoutmanager.add_article(data['article']);
			fetch_lock = false;
			
			if(isVisibleInView("#scroll-detect")) {
				fetch_article();
			}
			else {
				$("#scroll-detect").css("visibility", "hidden");
			}
		}
		else if(!data['success'] && data['article'] != null && data['article']['no_articles']) {
			//If no more articles to display
			$("#scroll-detect > div").css("display", "none");
			$("#scroll-detect > span").css("display", "block");
			//Do not remove the lock, since no more Ajax requests must be sent
		}
		else {
			//Remove the lock, if resulted in failure
			fetch_lock = false;
		}
	}, {"tab_id": get_active_tab(), "article_no": layoutmanager.no_of_articles});
}

/*
-------------------------
Utility functions
-------------------------
*/
function isVisibleInView(elem){
    var docViewTop = $(window).scrollTop();
    var docViewBottom = docViewTop + $(window).height();

    var elemTop = $(elem).offset().top;
    var elemBottom = elemTop + $(elem).height();

    return ((elemBottom <= docViewBottom) && (elemTop >= docViewTop));
}

function reload_tab() {
	layoutmanager.reset_layout();
	fetch_lock = false;
	fetch_article();
}

function get_active_tab(name) {
	var href = $("#sidebar-tabs > ul li.active a").get(0).href;
	var tab_name = $("#sidebar-tabs > ul li.active a").get(0).textContent;
	var tab_id = href.substring(href.lastIndexOf("/") + 1, href.length);
	
	if(arguments.length == 1){
		return tab_name.trim();
	}
	return tab_id;
}

/*
-------------------------
Source related functions
-------------------------
*/
function search_sources() {
	//If enter key was pressed or onclick of search button
	var query = $("#search-query").val();  //Get search query
	Dajaxice.newsreader.find_sources(function(data){
		$("#sources-results").empty(); //Delete any previous search results
		
		for (var i = 0; i < data["names"].length; i++) {
			$("#sources-results").append(htmlgenerator.generate_search_source_row(data["names"][i])); //Append the search result
		};
	}, {"query": query}); //Submit Ajax request
}

//Select or de-select a news source
function sources_select(source) {
	source.className = (source.className == "not-selected")? "selected success" : "not-selected";
}

//Gets all the selected news sources and sends an Ajax request to add it to the database
function add_sources() {
	//Get all the selected news sources
	var selected_rows = $("#sources-results").children(".selected");
	var selected_sources = [];
	var tab_id = get_active_tab();

	for (var i = 0; i < selected_rows.length; i++) {
		selected_sources[i] = selected_rows[i].cells[1].textContent;
		Dajaxice.newsreader.add_source(function(data){
			var success = data["success"];

			if(success)
				reload_tab();
		}, {"tab_id": tab_id, "source_name": selected_sources[i]});
	};

	//Hide the modal
	$("#add-source-modal").modal("hide");
}

/*
-------------------------
Tab related functions
-------------------------
*/
//Validates the add tab form to prevent null entries and large image size
function add_tab_validate(event, form) {
	event.preventDefault(); //Disable form submit
	
	//Validate tab name
	tab_name = form.children[1].value;
	if(tab_name.match(/^[a-zA-Z0-9\-_ ]+$/)) //Make sure name does not contain special characters
		form.submit(); //Submit the form
	
	return false; //Don't do anything
}

/*
-------------------------
Tag related functions
-------------------------
*/
function delete_tag(tag_element, link) {
	var tag = tag_element.textContent.trim().toLowerCase();
	var success = false;

	if(link == null) {
		var tab_id = get_active_tab();
		//Make Ajax call
		Dajaxice.tags.delete_tag(function(data) {
			success = data["success"];
			if(success) {
				delete_tag_element(tag_element);
				reload_tab();
			}
		}, {"tab_id": tab_id, "tag": tag});
	}
	else {
		Dajaxice.tags.delete_tag_from_article(function(data) {
			success = data["success"];
			if(success)
				delete_tag_element(tag_element);
		}, {"link": link, "tag": tag});
	}
}

function delete_tag_element(tag_element) {
	//Delete the html elements
	tag_element.parentElement.removeChild(tag_element.nextSibling);
	tag_element.parentElement.removeChild(tag_element);
}

//Retrieves tag predictions from the database and displays the results below the input box
function get_predictions(input) {
	var query = input.value.trim().toLowerCase(); //Remove any whitespaces and convert to lower case
	
	if(query) { //If the input is non-empty
		Dajaxice.tags.get_tags(function(data) {
			var results = data["tags"];
			var container = $(input.parentElement); //Get the parent element
			
			//Delete any previous tags
			container.children("span").remove();
			container.children("a").remove();

			//Append the results after the input box
			for(var i=0; i<((results.length > 7)? 7 : results.length); i++) {
				tag_elements = htmlgenerator.generate_tag(results[i], "add_tag(this.previousSibling)", false, true);
				container.append(tag_elements);
			};			
		}, {"query": query});
	}
}

//Creates a popover for the new tag button
function create_popover(element) {
	$(element).popover({
		'html': 'true',
		'trigger': 'manual',
		'placement': 'bottom',
		'content': function() {
			return $("#js-content").children()[2].outerHTML;
		}
	});
	$(element).popover('toggle');
}

//Sends Ajax call to insert the tag into the database and appends the tag to the current list of tags
function add_tag(tag_element) {
	var tag = tag_element.textContent.trim().toLowerCase();
	var tab_id = get_active_tab();

	Dajaxice.tags.add_tag(function(data){
		if(data["success"]) {
			append_tag(tag);
			delete_tag_element(tag_element);

			reload_tab();
		}
	}, {"tab_id": tab_id, "tag": tag});
}

//Appends the tag to the list of tags.
function append_tag(tag_name, article) {
	var new_tag_element = htmlgenerator.generate_tag(tag_name, "delete_tag(this.previousSibling, null)", true, true);
	
	if($("#tags>span:last").get(0) != undefined) //If there are already tags
		$("#tags>span:last").next().after(new_tag_element);
	else //If this is the first tag
		$($("#tags").children()[0]).before(new_tag_element);
}

//Retrieves the tags related to the tab
function retrieve_tags() {
	var tab_id = get_active_tab();
	
	if($(".tab-settings button").get(0).nextElementSibling == null) {//Perform Ajax only when showing the tab-settings popover
		Dajaxice.tags.get_tab_tags(function(data) {
			if(data["tags"] != null) {
				for(var i=0; i<data["tags"].length; i++) {
					append_tag(data["tags"][i]);
				};
			}
		},{"tab_id": tab_id});
	}
}

$( document ).ready(function() {
	
	//Initialize the HTMLGenerator and the LayoutManager
	htmlgenerator = new NTHtmlGenerator();
	var pattern = [
		{ "article_type": "featured", "no_repeat": "true" },
		{ "article_type": "portrait", "align": "left", "new_row": true },
		{ "article_type": "landscape", "align": "right" },
		{ "article_type": "landscape", "align": "right" },
		{ "article_type": "portrait", "align": "right", "new_row": true },
		{ "article_type": "landscape", "align": "left" },
		{ "article_type": "landscape", "align": "left" },
	];
	layoutmanager = new LayoutManager( ".newspaper-content", pattern, htmlgenerator.generate_article, htmlgenerator );
	fetch_article();

	//Fetches more articles when scrolling
	$( window ).scroll(function () {
		if( isVisibleInView( "#scroll-detect" ) ) {
			fetch_article();
		}
	});

	//Make tab list sortable. Uses JQuery UI Sortable plugin
	$( "#sidebar-tabs > ul" ).sortable({
		items: 'li',
		cursor: 'move',
		stop: function( event, ui ) {
			var tab_id = ui.item.children()[0].href;
			var sidebar_tabs = $( "#sidebar-tabs > ul" ).children( "li" );
			var new_position = 0;
			for (var i = 0; i < sidebar_tabs.length; i++) {
				var temp = $( sidebar_tabs[i] ).children()[0].href;
				var id = temp.substring( temp.lastIndexOf( "/" ) + 1, temp.length );
				if( temp == tab_id ) {
					new_position = i + 1;
					tab_id = id;
					break;
				}
			};
			
			//Ajax call
			Dajaxice.newsreader.change_tab_position( function( data ){}, { "tab_id": tab_id, "position": new_position } );
		}
	});

	//Tab settings popover
	$( ".tab-settings button" ).popover({
		'html': 'true',
		'placement': 'bottom',
		'title': '<strong>Tab Settings</strong>',
		'content': function() {
			return $( "#js-content" ).children()[0].outerHTML;
		}
	});

	//Add tab popover
	$( "#add-tab" ).popover({
		'trigger': 'click',
		'title': '<strong>Custom tab</strong><a class="close" href="#" onclick="$(\'#add-tab\').popover(\'hide\')">&times;</a>',
		'content': function() {
			return $( "#js-content" ).children()[1].outerHTML;
		},
		'html': 'true',
	});

	//Resend email
	if( $( "#resend-email" ).length > 0 ) {
		$( "#resend-email" ).click(function( event ){
			event.preventDefault();
			if ( !email_lock ) {
				email_lock = true;
				$( this ).next( "span" ).text( "Sending..." );
				
				Dajaxice.newsreader.resend_confirmation_mail(function( data ){
					if( data[ 'success' ] ){
						$( "#resend-email" ).next( "span" ).text( "Email sent!" );
					}
					else {
						$( "#resend-email" ).next( "span" ).text( "Error sending email. Try again!" );
						email_lock = false;
					}
				}, {});
			};
		});
	}
});

function retrieve_sources() {
	var tab_id = get_active_tab();
	Dajaxice.newsreader.get_sources(function(data){
		var source_list = data["sources"];
		$("#sources-dropdown>li").remove();
		for(var i=source_list.length-1; i>=0; i--){
			var element = $("#sources-dropdown");
			element.prepend(htmlgenerator.generate_source_element(source_list[i]));
		};
		
		$("#sources-dropdown").sortable({
			items: 'li',
			stop: function(event, ui) {
				var tab_id = get_active_tab();
				var source_name = ui.item.get(0).textContent;
				var position = 0;
				var children = $("#sources-dropdown").children();
				
				for(var i=0; i<children.length; i++) {
					if(children[i].textContent == source_name) {
						position = i + 1;
						break;
					}
				};

				Dajaxice.newsreader.change_source_position(function(data){
					console.log(data["success"]);
					if(data["success"]){
						console.log("Success. Reloading tab");
						reset_tab();
					}
				}, {
					"tab_id": tab_id, 
					"source_name": source_name.replace("×", "").trim(), 
					"position": position
				});
			}
		});

	}, {"tab_id": tab_id});
}

function display_delete_source(element, display) {
	element.children[0].style.display = (display)? "inline-block" : "none";
}

function delete_tab() {
	var tab_id = get_active_tab();
	var name = get_active_tab(true);
	
	if(confirm("Are you sure you want to delete " + name + "?")) {
		Dajaxice.newsreader.delete_tab(function(data){
			if(data["success"]) {
				var loc = document.location.toString();
				loc = loc.substring(0, loc.lastIndexOf("/"));
				document.location = loc;
			}
		}, {"tab_id": tab_id});
	}
}

function delete_source(element) {
	var source_name = element.textContent.replace("×", "").trim();
	var tab_id = get_active_tab();
	
	Dajaxice.newsreader.remove_source(function(data){
		if(data["success"]) {
			element.parentElement.delete;
			reset_tab();
		}
	}, {"tab_id": tab_id, "source_name": source_name});
}