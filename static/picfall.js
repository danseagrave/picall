
  //(trends are defined in the main html so that they can be set by the template system)

  var picstimer;
  var picsPaused = false;
  var picsCheckEverySeconds = 30;
  var picsurl = "/totallylive/justpics";
  
  //used to store trends when they fall off the list
  // just incase they get back on the list
  var pastTrendTweets = [];
  

 $(document).ready(function() {
   // do stuff when DOM is ready
   setupDHTML();
   startPics();

 });

function setupDHTML() {
  //add throbbers
  $("div.trendContainer h4").each(function(i) {
    addThrobber(this);
    addRemoveButton(this);
  });
}

function removeTrend(el) {
//  $(el).
}

function updateTrendPics(url, checkAgainSeconds) {
  //jQuery.each($("div.trendContainer"), function(){
  //early exit if we are paused
  if (picsPaused) {
    return;
  }
  
  jQuery.each(trends, function(){
    //trendName = $(this.id).attr("rel");
    trendId = "trend-" + this.position;
    trendName = this.name;
    
    picsContainer = $('#'+trendId).find("div.picContainer");
    
    //alert("pics span cnt: " + picsContainer.find("span.tweetPics:first").length);
    
    lastTweetID = picsContainer.find("span.tweetPics:first").eq(0).attr("rel");
    
    //setup since param
    sinceParam = ''
    if (lastTweetID) {
      sinceParam = "&since=" + lastTweetID
    }
    //start the thobber
    showThrobber($('#'+trendId).find("h4").eq(0));
    
    //get the pics
    params = "q="+encodeURIComponent(trendName) + sinceParam
    $.get(url, params, processResponse);
    
    //log params
    //$("#techData").prepend("fetching pics, params: " + params + "<br />");
  });
   
   //set a timer to check again - only if not paused
  if (!picsPaused) {
    picstimer = setTimeout("updateTrendPics(picsurl, "+checkAgainSeconds+")", checkAgainSeconds);
  }
}

function processResponse(data, status) { 
  //early exit if we are paused
  if (picsPaused) {
    return;
  }
  
  //process the response
  switch(status) {
  case "success":  
    
    //load the pic fragment
    var tempPicHolder = $("#tempPicHolder");
    tempPicHolder.html(data);
    
    //get the trend name from the fragment
    trendName = $("#tempPicHolder span.pics[rel]").eq(0).attr("rel");
        
    //find the right container to put the fragment in
    //TODO - need to fix something here - can't have apostophies in attributes - but can have them in trends...
    //     - maybe fix on client - load all trends into client side array (idx=>trend), then use idx as .trendContainer id
    //     - prob need to do this anyway - for the db powered version....
    picsContainer = $("div.trendContainer[rel="+trendName+"] div.picContainer").eq(0);
    
    //prepend the fragment to the container
    picsContainer.prepend(data);
    
    //add events
    attachViewTweetData(picsContainer);
    
    //update pic count
    updatePicCount(picsContainer);
    
    //hide the thobber
    hideThrobber(picsContainer.prev("h4").eq(0));
    break;
  
  default:
    $("#techData").prepend("sorry, twitter is slow <br />");
  }
}

function pausePics() {
  picsPaused = true;
  $("#startPicsButton").removeAttr("disabled");
  $("#pausePicsButton").attr("disabled", true);
  
}

function startPics() { 
  picsPaused = false;
 $("#startPicsButton").attr("disabled", true);
 $("#pausePicsButton").removeAttr("disabled");
  updateTrendPics(picsurl, picsCheckEverySeconds * 1000);
}

function addRemoveButton(target, extraClasses) {
  //add remove button
  targetJQ = $(target);
  targetJQ.append('<span class="removeTrend ' + extraClasses + '">[x]</span>');
  //set click action
  targetJQ.find(".removeTrend").click(function(el) { 
    container =  $(this).parents("div.trendContainer");
    pastTrendTweets[container.attr("rel")] = container;
    container.remove();
  });
}


function addThrobber(target, extraClasses) {
  $(target).append('<img class="throbber ' + extraClasses + '" src="/static/ajax-loader.gif" />');
}
function showThrobber(target) {
  $(target).find("img.throbber").show();
}
function hideThrobber(target) {
  $(target).find("img.throbber").hide();
}
function removeThrobber(target) {
  $(target).find("img.throbber").remove();
}

function updatePicCount(target) {
  //count
  var picCount = $(target).find("img").length;
  //update
  $(target).parent().find("span.picCount").html(picCount);
}

function attachViewTweetData(target) {
    //js for tweet data
    $(target).find("div.tweet").hover(viewTweetData, hideTweetData);
    //js for big pics
    $(target).find("div.tweet img").click(swapSrcRel);
}

function viewTweetData() {
    //alert("tweet data cnt: " + $(this).find(".tweetData").length);
    $(this).find(".tweetData").show();
}

function hideTweetData() {
    $(this).find(".tweetData").hide();
}

function swapSrcRel() {
    var img= $(this);
    var reltmp = img.attr("rel");
    //swap
    img.attr("rel", img.attr("src"));
    img.attr("src", reltmp);
}


