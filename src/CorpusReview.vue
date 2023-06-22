<template>
  <div id="app">
    <!-- 主体部分 -->

    <div id="corpus-review-area"></div>
  </div>
</template>

<script>
import * as d3 from "d3";
export default {
  name: "CorpusReview",
  props: ["title"],
  data() {
    return {
      width: 1000,
      height: 1000,
      colorList: [
        "red",
        "lightblue",
        "yellow",
        "green",
        "lightblue",
        "blue",
        "blue",
        "blue",
        "blue",
        "blue"
      ],
      testData: {
        links: [],
        nodes: []
      }
    };
  },
  methods: {
    initGraph(data) {
      let _this = this;
      let temp_list = null;
      temp_list = JSON.parse(JSON.stringify(data));
      // 异步获取数据
      this.axios.get("/getkeywordgraph?title=" + this.title).then(response => {
        let id_data, group_data, source_data, target_data, value_data;
        Object.keys(response.data.nodes).forEach(key => {
          id_data = response.data.nodes[key].id;
          group_data = response.data.nodes[key].group;
          temp_list.nodes.push({ id: id_data, group: group_data });
        });
        Object.keys(response.data.links).forEach(key => {
          source_data = response.data.links[key].source;
          target_data = response.data.links[key].target;
          value_data = response.data.links[key].value;
          temp_list.links.push({
            source: source_data,
            target: target_data,
            value: value_data
          });
        });
        console.log(temp_list);
        const links = temp_list.links
        const nodes = temp_list.nodes

        const simulation = d3
          .forceSimulation(nodes)
          .force(
            "link",
            d3
              .forceLink(links)
              .id(d => d.id)
              .distance(200)
          )
          .force("collide", d3.forceCollide().radius(() => 50))
          .force("charge", d3.forceManyBody().strength(-50))
          .force("center", d3.forceCenter(_this.width / 2, _this.height / 2));

        // const svg = d3.create("svg").attr("viewBox", [0, 0, width, height]);
        const svg = d3
          .select("#corpus-review-area")
          .append("svg")
          .attr("viewBox", [0, 0, _this.width, _this.height]);

        svg.call(d3.zoom().on("zoom", function() {
          g.attr("transform", d3.event.transform)
        }))

        const g = svg.append("g")

        const link = g
          .append("g")
          .attr("stroke", "#999")
          .attr("stroke-opacity", 0.6)
          .selectAll("line")
          .data(links)
          .join("line")
          .attr("stroke-width", d => Math.sqrt(d.value));

        const node = g
          .append("g")
          .selectAll("circle")
          .data(nodes)
          .join("circle")
          .attr("r", 35)
          .attr("class", "node")
          .attr("fill", _this.color)
          .call(_this.drag(simulation));

        node.append("title").text(d => d.id);

        const nodeText = g.append("g")
          .selectAll("text")
          .data(nodes)
          .join("text")
          .attr("dx", -30)
          .attr("dy", 6)
          .attr("class", "node-text")
          .text(function(d) {
            let temp_string = ""
            if (d.id.length <= 7) {
              temp_string = d.id
            }
            else {
              temp_string = d.id.substring(0, 7) + '...'
            }
            return temp_string
          })

        simulation.on("tick", () => {
          link
            .attr("x1", d => d.source.x)
            .attr("y1", d => d.source.y)
            .attr("x2", d => d.target.x)
            .attr("y2", d => d.target.y);

          node
            .attr("cx", d => d.x)
            .attr("cy", d => d.y);

          nodeText
            .attr("x", d => d.x)
            .attr("y", d => d.y)

        });
      });
    },
    color(d) {
      return this.colorList[d.group];
    },
    drag(simulation) {
      function dragstarted(d) {
        if (!d3.event.active) simulation.alphaTarget(0.3).restart();
        d.fx = d.x;
        d.fy = d.y;
      }

      function dragged(d) {
        d.fx = d3.event.x;
        d.fy = d3.event.y;
      }

      function dragended(d) {
        if (!d3.event.active) simulation.alphaTarget(0);
        d.fx = null;
        d.fy = null;
      }

      return d3
        .drag()
        .on("start", dragstarted)
        .on("drag", dragged)
        .on("end", dragended);
    }
  },
  beforeMount() {},
  mounted() {
    this.initGraph(this.testData);
  }
};
</script>

<style scoped>
/* 整体 */
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}
#app {
  /* font-family: Avenir, Helvetica, Arial, sans-serif; */
  /* -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale; */
  text-align: center;
  height: 100%;
  overflow: hidden;
}
.el-row {
  margin-top: 5vh;
  height: 70vh;
}
/* 左侧导航栏 */
#term-table {
  width: 100%;
  height: 70vh;
  background-color: #dbecff;
  border-radius: 5px;
  border: 2.8px rgb(225, 192, 255) solid;
}
/* 语料查看区域（中间） */
#corpus-review-area {
  width: 100%;
  height: 80vh;
  padding: 20px;
  overflow: none;
  border-right: 2.8px rgb(225, 192, 255) solid;
  border-left: 2.8px rgb(225, 192, 255) solid;
}
.el-col {
  border-radius: 4px;
}
</style>
<style>
.node {
  stroke-width: 3;
  stroke: rgb(140, 201, 250);
  cursor: pointer;
}
.node:hover {
  stroke: rgb(39, 76, 240);
  stroke-width: 8;
}
.node-text {
  font-size: 13px;
  overflow: hidden;
  word-wrap: normal;
}
</style>
