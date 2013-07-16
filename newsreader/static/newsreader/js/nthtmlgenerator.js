function NTHtmlGenerator() {
	this.classes = {
		"featured": "headlines row span9",
		"landscape": "span5",
		"portrait": "span4",
	};
};

NTHtmlGenerator.prototype.generate_clearfix = function() {
	return $( "<div>", { class: "clearfix" } );
};

NTHtmlGenerator.prototype.generate_tag = function(tag_name, onclick, delete_tag, black) {
	return $( "<span>", { 
		class: "label tag" + ( ( black )? "label-inverse" : "" ), 
		text: tag_name
	}).get(0).outerHTML + 
	$( "<a>", { 
		click: onclick, 
		html: ( delete_tag )? "&times;" : "+", 
		title: ( ( delete_tag )? "Delete" : "Add" ) + tag_name 
	}).get(0).outerHTML;
};

NTHtmlGenerator.prototype.generate_article = function(article, article_type, align) {
	var $article = 
	$( "<div>", { 
		class: ( ( align )? " nt-" + align + " " : "" ) + this.classes[article_type]
	})
	.append(
		//Generate the heading
		$( "<h3>", { class: "title" } )
		.append(
			$( "<a>", {
				href: article[ "link" ],
				text: article[ "title" ]
			})
		)
	)
	.append(
		//Generate byline
		$( "<div>", { class: "byline" } )
		.append( $( "<i>", { class: "icon-time" } ) )
		.append( article[ "pubDate" ] )
	)
	.append(
		//Generate the summary
		$( "<div>", { class: "article-content" } )
		.append( $( article[ "summary" ] ) )
		.append(
			$("<p>", { text: $("<p>").append(article["summary"]).text() } )
		)
	)
	.append( this.generate_clearfix() )
	.append( $( "<i>", { class: "icon-tag" } ) );
	
	//Generate tags
	var gen = this;
	$.each( article[ "tags" ], function( index, value ){ 
		$article.append( gen.generate_tag( value, "", true, false ) );
	});
	$article.append( this.generate_new_tag_element() );

	if(article_type == "featured")
		$article.append( this.generate_clearfix() );

	return $article.get(0).outerHTML;
};

NTHtmlGenerator.prototype.generate_search_source_row = function(source_name) {
	return $( "<tr>", {
		class: "not-selected",
	})
	.append(
		$( "<td>" ).append(
			$( "<i>", { class: "icon-ok" } )
		)
	)
	.append( $( "<td>", { text: source_name } ) )
	.attr( "onclick", "sources_select( this )" )
	.get(0).outerHTML;
};

NTHtmlGenerator.prototype.generate_new_tag_element = function() {
	return $( "<a>", { 
		onclick: "create_popover(this)" 
	})
	.append(
		$( "<span>", {
			class: "label label-info",
			text: "+ new tag"
		})
	);
}

NTHtmlGenerator.prototype.generate_source_element = function(source_name) {
	return $( "<li>" ).append(
		$( "<a>", { 
			text: source_name + "   ",
			css: "word-wrap: break-word; white-space: normal;",
			href: "#"
		})
		.append(
			$( "<span>", {
				title: "Delete " + source_name,
				style: "font-size: 1.4em; color: red; font-weight: bolder;",
				html: "&times;"
			})
			.attr( "onclick", "delete_source( this.parentElement )" )
		)
		.attr( "role", "menuitem" )
	).get(0).outerHTML;
}