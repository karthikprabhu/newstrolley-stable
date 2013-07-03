// generate_article(article, article_type, alignment)
// pattern_format = [
// 	{"article_type": "featured,portrait,landscape", "align": "left/right", "new_row": "true/false"};
// ]
function LayoutManager(container, pattern, generate_article, context) {
	this.no_of_articles = 1;
	this.current_row = 0;
	this.position_index = 1;

	this.container = container;
	this.pattern = pattern;
	this.generate_article = generate_article;
	this.context = (context == undefined)? this : context;

	this.no_repeat = {};

	//Resets the layout variables and empties the container
	this.reset_layout = function() {
		this.no_of_articles = 1;
		this.current_row = 0;
		this.position_index = 1;
		this.no_repeat = {};
		$(this.container).empty();
	}

	//Gets the next position from the pattern
	this.get_next_position = function() {
		var index = (this.position_index - 1) % this.pattern.length;
		if(index == -1) index = 5;
		return this.pattern[index];
	}

	this.create_new_row = function() {
		this.current_row++;
		$("<div/>", {
			id: "row-" + this.current_row,
			class: "row"
		}).appendTo(this.container);
	}

	//Adds a new article to the layout
	this.add_article = function(article) {
		var position = this.get_next_position();
		var content = '';

		if("no_repeat" in position && position["no_repeat"]) {
			if(this.no_repeat[position]) { //Skip this pattern
				this.position_index++
				position = this.get_next_position();
			}
			else { //Add to the list of no_repeat
				this.no_repeat[position] = true;
			}
		}

		if("new_row" in position && position["new_row"]) {
			this.create_new_row();
		}

		if("article_type" in position) {
			content += this.generate_article.call(this.context, article, position["article_type"], (("align" in position)? position["align"] : ""));
		}

		if("article_type" in position && position["article_type"] == "featured") {
			$(this.container).append(content);
		}
		else {
			$("#row-" + this.current_row).append(content);
		}

		this.no_of_articles++;
		this.position_index++;
	}
}