package servlets;

import java.io.IOException;
import java.io.PrintWriter;
import java.io.StringReader;
import java.util.List;

import javax.servlet.ServletConfig;
import javax.servlet.ServletContext;
import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

import org.json.JSONArray;
import org.json.JSONObject;

import edu.stanford.nlp.ling.HasWord;
import edu.stanford.nlp.ling.TaggedWord;
import edu.stanford.nlp.parser.nndep.DependencyParser;
import edu.stanford.nlp.process.DocumentPreprocessor;
import edu.stanford.nlp.tagger.maxent.MaxentTagger;
import edu.stanford.nlp.trees.GrammaticalStructure;
import edu.stanford.nlp.trees.TypedDependency;

/**
 * Servlet implementation class UniversalDependencies
 */
@WebServlet("/dependencies")
public class UniversalDependencies extends HttpServlet {
	private static final long serialVersionUID = 1L;

	/**
	 * Default constructor.
	 */
	public UniversalDependencies() {
		// TODO Auto-generated constructor stub
	}

	private ServletContext ctx = null;

	@Override
	public void init(ServletConfig config) throws ServletException {
		ctx = config.getServletContext();
	}

	/**
	 * @see HttpServlet#doGet(HttpServletRequest request, HttpServletResponse
	 *      response)
	 */
	protected void doPost(HttpServletRequest request, HttpServletResponse response)
			throws ServletException, IOException {

		String modelPath = DependencyParser.DEFAULT_MODEL;
		String taggerPath = "edu/stanford/nlp/models/pos-tagger/english-left3words/english-left3words-distsim.tagger";

		String text = request.getParameter("text");

		if (text == null) {
			response.setContentType("application/json");
			PrintWriter out = response.getWriter();
			response.setStatus(HttpServletResponse.SC_FORBIDDEN);
			out.print(new JSONObject("{\"error\":\"No input string\"}"));
			out.flush();
			return;
		}

		if (ctx.getAttribute("tagger") == null) {
			MaxentTagger tagger = new MaxentTagger(taggerPath);
			DependencyParser parser = DependencyParser.loadFromModelFile(modelPath);

			ctx.setAttribute("tagger", tagger);
			ctx.setAttribute("parser", parser);
		}

		response.setContentType("application/json");
		PrintWriter out = response.getWriter();
		JSONObject objects = getDependencies((MaxentTagger) ctx.getAttribute("tagger"),
				(DependencyParser) ctx.getAttribute("parser"), text);
		out.print(objects);
		out.flush();
	}

	/**
	 * @see HttpServlet#doPost(HttpServletRequest request, HttpServletResponse
	 *      response)
	 */
	protected void doGet(HttpServletRequest request, HttpServletResponse response)
			throws ServletException, IOException {
		// TODO Auto-generated method stub
	}

	private JSONObject getDependencies(MaxentTagger tagger, DependencyParser parser, String text) {

		JSONArray sentences = new JSONArray();
		JSONObject list = new JSONObject();
		
		DocumentPreprocessor tokenizer = new DocumentPreprocessor(new StringReader(text));
		for (List<HasWord> sentence : tokenizer) {
			List<TaggedWord> tagged = tagger.tagSentence(sentence);
			GrammaticalStructure gs = parser.predict(tagged);

			JSONArray posTagger = new JSONArray();
			for (TaggedWord word : tagged) {
				JSONObject taggerObj = new JSONObject();
				taggerObj.put("word", word.word());
				taggerObj.put("tag", word.tag());
				posTagger.put(taggerObj);

			}

			JSONArray universalDependency = new JSONArray();
			for (TypedDependency dep : gs.typedDependenciesCollapsed()) {
				JSONObject obj = new JSONObject();
				obj.put("reln", dep.reln());
				obj.put("gov", dep.gov().word());
				obj.put("dep", dep.dep().word());
				universalDependency.put(obj);
			}
			
			JSONObject json = new JSONObject();
			json.put("sentence", sentence.toString());
			json.put("pos", posTagger);
			json.put("dependencies", universalDependency);
//			json.put("review", text);

			sentences.put(json);
		}

		list.put("list", sentences);
		list.put("review", text);
		
		return list;
	}

}