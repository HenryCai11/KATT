<template>
  <div id="app">
    <!-- 右侧分析栏 -->
    <div id="analysis-table">
      <div id="basic-info">
        字数统计：{{ wordcount }}
        <br />
      </div>
      <div id="doc-graph"></div>
    </div>
  </div>
</template>

<script>
import "es6-promise/auto";
import * as d3 from "d3";

export default {
  name: "RightDocuments",
  data() {
    return {
      bardata: "test",
      testModel: "",
      docList: {
        nodes: []
      },
      width: 300,
      height: 350,
      wordcount: null,
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
      ]
    };
  },
  methods: {
    initGraph(data) {
      let _this = this;
      let temp_list = null;
      temp_list = JSON.parse(JSON.stringify(data));
      // 异步获取数据
      this.axios.get("/getdocgraph").then(response => {
        let id_data, group_data, word_count;
        Object.keys(response.data.nodes).forEach(key => {
          id_data = response.data.nodes[key].id;
          group_data = response.data.nodes[key].group;
          word_count = response.data.nodes[key].wordcount;
          temp_list.nodes.push({ id: id_data, group: group_data, wordcount: word_count });
        });
        const nodes = temp_list.nodes;

        const simulation = d3
          .forceSimulation(nodes)
          // .force(
          //   "link",
          //   d3
          //     .forceLink(links)
          //     .id(d => d.id)
          //     .distance(100)
          // )
          .force("charge", d3.forceManyBody())
          .force("center", d3.forceCenter(_this.width / 2, _this.height / 2));

        // const svg = d3.create("svg").attr("viewBox", [0, 0, width, height]);
        const svg = d3
          .select("#doc-graph")
          .append("svg")
          .attr("viewBox", [0, 0, _this.width, _this.height]);

        svg.call(
          d3.zoom().on("zoom", function() {
            g.attr("transform", d3.event.transform);
          })
        );

        const g = svg.append("g");

        // const link = g
        //   .append("g")
        //   .attr("stroke", "#999")
        //   .attr("stroke-opacity", 0.6)
        //   .selectAll("line")
        //   .data(links)
        //   .join("line")
        //   .attr("stroke-width", d => Math.sqrt(d.value));

        const node = g
          .append("g")
          .attr("stroke", "#fff")
          .attr("stroke-width", 1.5)
          .attr("class", "node")
          .selectAll("circle")
          .data(nodes)
          .join("circle")
          .attr("r", 30)
          .attr("fill", _this.color)
          .on("click", function(d) {
            _this.wordcount = d.wordcount
          })
          .call(_this.drag(simulation));

        node.append("title").text(d => d.id);

        const nodeText = g
          .append("g")
          .selectAll("text")
          .data(nodes)
          .join("text")
          .attr("dx", -15)
          .attr("dy", 6)
          .attr("class", "node-text")
          .text(function(d) {
            return d.id;
          });

        simulation.on("tick", () => {
          // link
          //   .attr("x1", d => d.source.x)
          //   .attr("y1", d => d.source.y)
          //   .attr("x2", d => d.target.x)
          //   .attr("y2", d => d.target.y);

          node.attr("cx", d => d.x).attr("cy", d => d.y);

          nodeText.attr("x", d => d.x).attr("y", d => d.y);
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
  mounted() {
    this.initGraph(this.docList);
  }
};
</script>

<style scoped>
.el-row {
  margin-top: 5vh;
  height: 70vh;
}
#analysis-table {
  width: 100%;
  height: 70vh;
  background-color: #dbecff;
  border-radius: 5px;
  border: 2.8px rgb(225, 192, 255) solid;
  display: flex;
  justify-content: center;
  align-items: center;
  flex-direction: column;
}
#basic-info {
  height: 20%;
  width: 80%;
  text-align: left;
}
#doc-graph {
  height: 70%;
  width: 100%;
}
.el-col {
  border-radius: 4px;
}
</style>
<style>
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
}
</style>
