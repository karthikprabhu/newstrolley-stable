function NTHtmlGenerator() {
};

NTHtmlGenerator.prototype.generate_clearfix = function() {
	var clearfix = document.createElement("div");
	clearfix.className = "clearfix";

	return clearfix;
};

NTHtmlGenerator.prototype.generate_tag = function(tag_name, onclick, delete_tag, black) {
	var tag = document.createElement("span");
	tag.className = "label tag" + ((black)? " label-inverse" : "");
	tag.innerHTML = tag_name;
	
	var tag_anchor = document.createElement("a");
	tag_anchor.setAttribute("onclick", onclick);
	if (delete_tag) {
		tag_anchor.setAttribute("title", "Delete " + tag_name);
		tag_anchor.innerHTML = "&times;";
	}
	else {
		tag_anchor.setAttribute("title", "Add " + tag_name);
		tag_anchor.innerHTML = "+";
	}

	return [tag, tag_anchor];
};

NTHtmlGenerator.prototype.generate_article = function(article, article_type, align) {
	var article_container = document.createElement("div");
	var classes = {
		"featured": "headlines row span9",
		"landscape": "span5",
		"portrait": "span4",
	};
	article_container.className = ((align)? " nt-" + align + " " : "") + classes[article_type];

	/*
	---------------
	Generate the heading
	---------------
	*/
	var article_heading = document.createElement("h3");
	article_heading.className = "title";

	var heading_anchor = document.createElement("a");
	heading_anchor.setAttribute("href", article["link"]);
	heading_anchor.innerHTML = article["title"];
	article_heading.appendChild(heading_anchor);

	article_container.appendChild(article_heading);

	/*
	---------------
	Generate byline
	---------------
	*/
	var article_byline = document.createElement("div");
	article_byline.className = "byline";

	var byline_icon = document.createElement("i");
	byline_icon.className = "icon-time";
	
	var pub_date = document.createTextNode(" " + article["pubDate"]);
	
	article_byline.appendChild(byline_icon);
	article_byline.appendChild(pub_date);
	
	article_container.appendChild(article_byline);

	/*
	---------------
	Generate the summary
	---------------
	*/
	var article_summary = document.createElement("div");
	article_summary.className = "article-content";

	var summary_p = document.createElement("p");
	summary_p.innerHTML += article["summary"];
	
	if(summary_p.children.length)
		article_summary.appendChild(summary_p.children[0]);
	article_summary.appendChild(summary_p);	
	
	article_container.appendChild(article_summary);
	article_container.appendChild(this.generate_clearfix());

	/*
	---------------
	Generate the tags
	---------------
	*/
	var tag_icon = document.createElement("i");
	tag_icon.className = "icon-tag";
	
	article_container.appendChild(tag_icon);
	article_container.appendChild(document.createTextNode(" "));

	var tags = article["tags"];
	for (var i = 0; i < tags.length; i++) {
		var temp = this.generate_tag(tags[i], "", true, false);
		article_container.appendChild(temp[0]);
		article_container.appendChild(temp[1]);
	};
	article_container.appendChild(this.generate_new_tag_element());

	if(article_type == "featured")
		article_container.appendChild(this.generate_clearfix());

	return article_container.outerHTML;
};

NTHtmlGenerator.prototype.generate_search_source_row = function(source_name) {
	var row = document.createElement("tr");
	row.className = "not-selected";
	row.setAttribute("onclick", "sources_select(this)");

	var column1 = document.createElement("td");
	var tick_icon = document.createElement("i");
	tick_icon.className = "icon-ok";
	column1.appendChild(tick_icon);

	var column2 = document.createElement("td");
	var source_text = document.createTextNode(source_name);
	column2.appendChild(source_text)
	
	row.appendChild(column1);
	row.appendChild(column2);
	
	return row.outerHTML;
};

NTHtmlGenerator.prototype.generate_new_tag_element = function() {
	var anchor = document.createElement("a");
	anchor.setAttribute("onclick", "create_popover(this)");

	var span = document.createElement("span");
	span.className = "label label-info";
	span.innerHTML = "+ new tag";
	anchor.appendChild(span);

	return anchor;
}

NTHtmlGenerator.prototype.generate_source_element = function(source_name) {
	var list_element = document.createElement("li");

	var anchor = document.createElement("a");
	anchor.setAttribute("role", "menuitem");
	anchor.setAttribute("style", "word-wrap: break-word; white-space:normal;");

	var text = document.createTextNode(source_name + "   ");
	anchor.appendChild(text);

	var span = document.createElement("span");
	span.setAttribute("style", "font-size:1.4em; color:red; font-weight: bolder;");
	span.setAttribute("onclick", "delete_source(this.parentElement)");
	span.setAttribute("title", "Delete " + source_name);
	span.innerHTML = "&times;";
	anchor.appendChild(span);

	list_element.appendChild(anchor);

	return list_element.outerHTML;
}