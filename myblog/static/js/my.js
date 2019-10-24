
    function onAddCategoryClick(obj) {
        var cates = document.getElementsByName("categories");

        var word = prompt("please input new category name","");
        var i;
        if(word.length == 0)
            return false;
        for(i=0;i<cates.length;i++)
        {

            if(cates[i].value == word)
            {
                alert("分类已存在");
                return false;
            }
        }
        var newTag = document.createElement("input")
        var newLabel = document.createElement("label");
        newLabel.innerText = word+"  :  ";
        newTag.type = "radio" ;
        newTag.name = "categories" ;
        newTag.value = word;
        obj.insertAdjacentElement('beforebegin',newLabel);
        newLabel.insertAdjacentElement('beforebegin',newTag);
        return false;
    }
     function onAddTagClick(obj) {
  var tags = document.getElementsByName("tags");

        var word = prompt("please input new tag name","");
        var i;
        if(word.length == 0)
            return false;
        for(i=0;i<tags.length;i++)
        {
            if(tags[i].value == word)
            {
                alert("标签已存在");
                return false;
            }
        }
        var newTag = document.createElement("input")
        var newLabel = document.createElement("label");
        newLabel.innerText = word+"  :  ";
        newTag.type = "checkbox" ;
        newTag.name = "tags" ;
        newTag.value = word;
        obj.insertAdjacentElement('beforebegin',newLabel);
        newLabel.insertAdjacentElement('beforebegin',newTag);

        return false;
    }
    function onNewPostSubmitClick()
    {
        var cates = document.getElementsByName("categories");
        var tags = document.getElementsByName("tags");
        var cate_selected = 0;
        var tag_select = 0 ;

        for(var i=0 ; i<cates.length;i++)
        {
            if(cates[i].checked)
            {
                cate_selected = 1;
                break;
            }
        }

        for(var i=0 ; i<tags.length;i++)
        {
            if(tags[i].checked)
            {
                tag_select = 1;
                break;
            }
        }

        if(cate_selected&&tag_select)
        {

            return true;
        }
        alert("please choose category and tags for the post");
        return false;
    }
