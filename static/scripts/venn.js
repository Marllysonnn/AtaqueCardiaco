am5.ready(function() {

    // Create root
    var root = am5.Root.new("chartvenn");
  
    // Set themes
    root.setThemes([ 
      am5themes_Animated.new(root)
    ]);
  
    // Create wrapper container
    var container = root.container.children.push(am5.Container.new(root, {
      width: am5.p100,
      height: am5.p100,
      layout: root.verticalLayout
    }));
   
    // Create venn series
    var chart = container.children.push(am5venn.Venn.new(root, {
      categoryField: "name",
      valueField: "value",
      intersectionsField: "sets",
      paddingTop: 40,
      paddingBottom: 40,
      paddingLeft: 40,
      paddingRight: 40
    }));
  
    var pattern = am5.CirclePattern.new(root, {
      fill: am5.color(0x000000),
      color: am5.color(0xffffff),
      radius: 10,
      gap: 10,
      checkered: true
    })
  
    chart.slices.template.setAll({ templateField: "sliceSettings" });
    chart.labels.template.set("fill", am5.color(0xffffff));
    chart.labels.template.setup = function(target) {
      target.set("background", am5.RoundedRectangle.new(root, {
        stroke: am5.color(0xffffff),
        fill: am5.color(0x000000),
        cornerRadiusTL: 5,
        cornerRadiusTR: 5,
        cornerRadiusBL: 5,
        cornerRadiusBR: 5,
        fillOpacity: 1
      }));
    }
  
    // Fetch data from Flask server
    fetch('/dados_venn')
      .then(response => response.json())
      .then(data => {
        // Multiply values by a factor to adjust circle size
        data.forEach(item => {
          item.value *= 2; // Adjust the factor as needed
        });
  
        // Set data for the Venn chart
        chart.data.setAll(data);
      })
      .catch(error => {
        console.error('Error fetching data:', error);
      });
  
    // Set up hover appearance
    chart.hoverGraphics.setAll({
      strokeDasharray: [3, 3],
      stroke: am5.color(0xffffff),
      strokeWidth: 2
    });
  
  }); // end am5.ready()
  