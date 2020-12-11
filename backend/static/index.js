function timeSince(date) {
    var now = new Date();
    var diff = now.getTimezoneOffset() * 60 * 1000;

    var seconds = Math.floor((now.valueOf() - date + diff ) / 1000);
    
    // console.log(seconds);
    if(seconds < 0) seconds -= Math.floor(diff/1000);


    var interval = Math.floor(seconds / 31536000);
  
    if (interval > 1) {
      return interval + " лет назад";
    }
    interval = Math.floor(seconds / 2592000);
    if (interval > 1) {
      return interval + " месяцев назад";
    }
    interval = Math.floor(seconds / 86400);
    if (interval > 1) {
      return interval + " дней назад";
    }
    interval = Math.floor(seconds / 3600);
    if (interval > 1) {
      return interval + " часов назад";
    }
    interval = Math.floor(seconds / 60);
    if (interval > 1) {
      return interval + " минут назад";
    }
    return Math.floor(seconds) + " секунд назад";
}

var zoom = (function () {
    var scale = 1, recurLev = 0;
    function alter(fn, adj) {
        var original = $.fn[fn];
        $.fn[fn] = function () {
            var result;
            recurLev += 1;
            try {
                result = original.apply(this, arguments);
            } finally {
                recurLev -= 1;
            }
            if (arguments.length === 0 && recurLev === 0) {
                result = adj(result);
            }
            return result;
        };
    }
    function scalePos(n) { return n / scale; }
    /* Not needed since jQuery 3.2.0
    alter("width", scalePos);
    alter("height", scalePos);
    alter("outerWidth", scalePos);
    alter("outerHeight", scalePos);
    alter("innerWidth", scalePos);
    alter("innerHeight", scalePos);
    */
    alter("offset", function (o) { o.top /= scale; o.left /= scale; return o; });
    return function (s) {
        scale = s;
        document.body.style.transform = "scale(" + scale + ")";
        document.body.style.transformOrigin = "top left";
        document.body.style.width = (100 / scale) + "%";
        document.body.style.height = (100 / scale) + "%";
    };
}());

function init_popup(table){
    if(!table) table = $(document);

    table.find(".graph-show-btn").each(function(index){
        $(this).popup({
            html    : `Кликни для просмотра графика`
        });
    });

    table.find(".prevyear").each(function(index){
        let data = $(this).data("prev");
        
        $(this).text(data[2]);

        $(this).popup({
            html    : `
                <div class="ui three column divided center aligned grid">
                <div class="column">2017<br>${data[0]}</div>
                <div class="column">2018<br>${data[1]}</div>
                <div class="column">2019<br>${data[2]}</div>
                </div>`
        });
    });

    table.find('.popup-places').each(function(index){
        let olymp = $(this).data("olymp_cnt")
        let free = $(this).text()
        $(this).popup({
            html    : `
                <div class="ui three column divided center aligned grid">
                <div class="column">МЕСТ<br>${parseInt(olymp)+parseInt(free)}</div>
                <div class="column">БВИ<br>${olymp}</div>
                <div class="column">ОК<br>${free}</div>
                </div>`
        });
    });
}
const Points_DEFAULT = 321;
let Points = Points_DEFAULT;
const DISCIP_DEFAULT = 2147483647; 
let Discip = DISCIP_DEFAULT;

function filter(points, discip){

    // if(points == 321) return;
    $(".univer-item").each(function(){
        let cnt = 0;
        $(this).find("table tbody tr").each(function(){
            let current_discip = parseInt( $(this).data("discip"));
            // console.log("current dis: ", current_discip, " dis: ", discip, " curr&dis ", discip&current_discip);
            let check_points = (parseInt( $(this).find(".lastscore").text() ) <= points);
            let check_disciplines = (discip&current_discip) == current_discip;

            if( (check_points || Points==Points_DEFAULT) && (check_disciplines || Discip==DISCIP_DEFAULT) ){
                $(this).show();
                cnt++;
            }else{
                $(this).hide();                
            }
        });
        if(cnt) 
            $(this).show();
        else
            $(this).hide();

        $(this).find(".fac-cnt").text(cnt);

    });

}

function recalc_discip(){
    let vals = $(".dropdown input[type='hidden']").attr("value").split(",");
    Discip = 0;
    for(var elem in vals ){
        Discip += parseInt(vals[elem]);
    }

    // check if Discip is None
    if(!Discip) Discip = DISCIP_DEFAULT;
    
    filter(Points, Discip);
}


$(function(){
    function recalc_discip(){
        let vals = $(".dropdown input[type='hidden']").attr("value").split(",");
        Discip = 0;
        for(var elem in vals ){
            Discip += parseInt(vals[elem]);
        }
    
        // check if Discip is None
        if(!Discip) Discip = DISCIP_DEFAULT;
        
        filter(Points, Discip);
    }

    $('.time-update').each(function(index){
        $(this).text( timeSince( $(this).data("time") ) );
    });
    

    $('thead th.int').data('sortBy', function(th, td, tablesort) {
        return parseInt(td.text(), 16);
    });

    $(".datetimefromcurr").each(function(index){
        $(this).text( timeSince( $(this).text() ) );
    });

    $(".lastscore").each(function(index){
        let data = $(this).data("lscore");
        
        $(this).text(data[data.length - 1][1]);
    });

    init_popup();
    $('table').on('tablesort:complete', function(event, tablesort) {
        init_popup( $(this) );
        // console.log($(this) );
    });

    $('table').tablesort();
    
    $(".content-show-btn").on('click', function(){
        $(this).closest(".univer-item").children(".hidden_table").transition('toggle');
        // $(this).html("<i class='arrow up icon'></i>");

        $(this).html($(this).html() == '<i class="angle down icon"></i>' ? '<i class="angle up icon"></i>' : '<i class="angle down icon"></i>');

    });
    
    $(".graph-show-btn").on('click', function(){
        let lscore = $(this).data("lscore");
        let data_x = [];
        let data_y = [];

        // console.log(data_x);
        // console.log(data_y);


        for(var i = 0; i < lscore.length; i++)
        {
        data_x.push(lscore[i][0]);
        data_y.push(lscore[i][1]);
        }

        $(".modal").modal({
            onShow : function(){
                var data = [
                    {
                      x: data_x,
                      y: data_y,
                      type: 'scatter'
                    }
                  ];
                  
                Plotly.newPlot('PLOT', data);
            },
            onHide : function(){
                Plotly.purge('PLOT');
            }
        })
        .modal("show");

    });

   
    recalc_discip();
    $('.ui.dropdown').dropdown({
        onChange: recalc_discip,
    });




    var softSlider = document.getElementById('soft');

    noUiSlider.create(softSlider, {
        start: 321,
        step:1,
        range: {
            min: 0,
            max: 325
        },
        tooltips: true,
        connect: [true,false],
        padding: 6,

        pips: {
            mode: 'values',
            values: [0, 100,200,275,325],
            density: 3
        },
        format: {
            to: function (value) {
                return parseInt(value);
            },
            from: function (value) {
                return parseInt(value);
            }
        }
    });

    softSlider.noUiSlider.on('change', function (values, handle) {
        // console.log(values[handle]);

        Points = parseInt(values[handle]); 
        filter(Points, Discip);
    });


});
