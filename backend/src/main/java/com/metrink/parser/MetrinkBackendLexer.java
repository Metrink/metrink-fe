// Generated from /home/wspeirs/src/metrink-fe/MetrinkBackend.g4 by ANTLR 4.7
package com.metrink.parser;
import org.antlr.v4.runtime.Lexer;
import org.antlr.v4.runtime.CharStream;
import org.antlr.v4.runtime.Token;
import org.antlr.v4.runtime.TokenStream;
import org.antlr.v4.runtime.*;
import org.antlr.v4.runtime.atn.*;
import org.antlr.v4.runtime.dfa.DFA;
import org.antlr.v4.runtime.misc.*;

@SuppressWarnings({"all", "warnings", "unchecked", "unused", "cast"})
public class MetrinkBackendLexer extends Lexer {
	static { RuntimeMetaData.checkVersion("4.7", RuntimeMetaData.VERSION); }

	protected static final DFA[] _decisionToDFA;
	protected static final PredictionContextCache _sharedContextCache =
		new PredictionContextCache();
	public static final int
		DO=1, FOR=2, GT=3, LT=4, GT_EQ=5, LT_EQ=6, DB_EQ=7, PIPE=8, COPY_PIPE=9, 
		AMP=10, METRIC=11, LOG=12, EVENT=13, LPAREN=14, RPAREN=15, LBRACKET=16, 
		RBRACKET=17, LBRACE=18, RBRACE=19, COMMA=20, EQUAL=21, PLUS=22, MINUS=23, 
		MUL=24, DIV=25, REM=26, COLON=27, TIME_INDICATOR=28, PM_INDICATOR=29, 
		AM_INDICATOR=30, TRUE=31, FALSE=32, IDENTIFIER=33, POSITIVE_INTEGER_LITERAL=34, 
		FLOATING_POINT_LITERAL=35, REGEX_LITERAL=36, STRING_LITERAL=37, QUOTE=38, 
		WS=39;
	public static String[] channelNames = {
		"DEFAULT_TOKEN_CHANNEL", "HIDDEN"
	};

	public static String[] modeNames = {
		"DEFAULT_MODE"
	};

	public static final String[] ruleNames = {
		"DO", "FOR", "GT", "LT", "GT_EQ", "LT_EQ", "DB_EQ", "PIPE", "COPY_PIPE", 
		"AMP", "METRIC", "LOG", "EVENT", "LPAREN", "RPAREN", "LBRACKET", "RBRACKET", 
		"LBRACE", "RBRACE", "COMMA", "EQUAL", "PLUS", "MINUS", "MUL", "DIV", "REM", 
		"COLON", "TIME_INDICATOR", "PM_INDICATOR", "AM_INDICATOR", "TRUE", "FALSE", 
		"IDENTIFIER", "POSITIVE_INTEGER_LITERAL", "FLOATING_POINT_LITERAL", "REGEX_LITERAL", 
		"STRING_LITERAL", "QUOTE", "WS", "SCharSequence", "SChar"
	};

	private static final String[] _LITERAL_NAMES = {
		null, "'DO'", "'FOR'", "'>'", "'<'", "'>='", "'<='", "'=='", "'|'", "'>|'", 
		"'&'", null, null, null, "'('", "')'", "'['", "']'", "'{'", "'}'", "','", 
		"'='", "'+'", "'-'", "'*'", "'/'", "'%'", "':'"
	};
	private static final String[] _SYMBOLIC_NAMES = {
		null, "DO", "FOR", "GT", "LT", "GT_EQ", "LT_EQ", "DB_EQ", "PIPE", "COPY_PIPE", 
		"AMP", "METRIC", "LOG", "EVENT", "LPAREN", "RPAREN", "LBRACKET", "RBRACKET", 
		"LBRACE", "RBRACE", "COMMA", "EQUAL", "PLUS", "MINUS", "MUL", "DIV", "REM", 
		"COLON", "TIME_INDICATOR", "PM_INDICATOR", "AM_INDICATOR", "TRUE", "FALSE", 
		"IDENTIFIER", "POSITIVE_INTEGER_LITERAL", "FLOATING_POINT_LITERAL", "REGEX_LITERAL", 
		"STRING_LITERAL", "QUOTE", "WS"
	};
	public static final Vocabulary VOCABULARY = new VocabularyImpl(_LITERAL_NAMES, _SYMBOLIC_NAMES);

	/**
	 * @deprecated Use {@link #VOCABULARY} instead.
	 */
	@Deprecated
	public static final String[] tokenNames;
	static {
		tokenNames = new String[_SYMBOLIC_NAMES.length];
		for (int i = 0; i < tokenNames.length; i++) {
			tokenNames[i] = VOCABULARY.getLiteralName(i);
			if (tokenNames[i] == null) {
				tokenNames[i] = VOCABULARY.getSymbolicName(i);
			}

			if (tokenNames[i] == null) {
				tokenNames[i] = "<INVALID>";
			}
		}
	}

	@Override
	@Deprecated
	public String[] getTokenNames() {
		return tokenNames;
	}

	@Override

	public Vocabulary getVocabulary() {
		return VOCABULARY;
	}


	public MetrinkBackendLexer(CharStream input) {
		super(input);
		_interp = new LexerATNSimulator(this,_ATN,_decisionToDFA,_sharedContextCache);
	}

	@Override
	public String getGrammarFileName() { return "MetrinkBackend.g4"; }

	@Override
	public String[] getRuleNames() { return ruleNames; }

	@Override
	public String getSerializedATN() { return _serializedATN; }

	@Override
	public String[] getChannelNames() { return channelNames; }

	@Override
	public String[] getModeNames() { return modeNames; }

	@Override
	public ATN getATN() { return _ATN; }

	public static final String _serializedATN =
		"\3\u608b\ua72a\u8133\ub9ed\u417c\u3be7\u7786\u5964\2)\u0103\b\1\4\2\t"+
		"\2\4\3\t\3\4\4\t\4\4\5\t\5\4\6\t\6\4\7\t\7\4\b\t\b\4\t\t\t\4\n\t\n\4\13"+
		"\t\13\4\f\t\f\4\r\t\r\4\16\t\16\4\17\t\17\4\20\t\20\4\21\t\21\4\22\t\22"+
		"\4\23\t\23\4\24\t\24\4\25\t\25\4\26\t\26\4\27\t\27\4\30\t\30\4\31\t\31"+
		"\4\32\t\32\4\33\t\33\4\34\t\34\4\35\t\35\4\36\t\36\4\37\t\37\4 \t \4!"+
		"\t!\4\"\t\"\4#\t#\4$\t$\4%\t%\4&\t&\4\'\t\'\4(\t(\4)\t)\4*\t*\3\2\3\2"+
		"\3\2\3\3\3\3\3\3\3\3\3\4\3\4\3\5\3\5\3\6\3\6\3\6\3\7\3\7\3\7\3\b\3\b\3"+
		"\b\3\t\3\t\3\n\3\n\3\n\3\13\3\13\3\f\3\f\3\f\3\f\3\f\3\f\3\f\5\fx\n\f"+
		"\3\r\3\r\3\r\3\r\5\r~\n\r\3\16\3\16\3\16\3\16\5\16\u0084\n\16\3\17\3\17"+
		"\3\20\3\20\3\21\3\21\3\22\3\22\3\23\3\23\3\24\3\24\3\25\3\25\3\26\3\26"+
		"\3\27\3\27\3\30\3\30\3\31\3\31\3\32\3\32\3\33\3\33\3\34\3\34\3\35\3\35"+
		"\3\36\3\36\3\36\3\37\3\37\3\37\3 \3 \3 \3 \3 \3 \3 \3 \5 \u00b2\n \3!"+
		"\3!\3!\3!\3!\3!\3!\3!\3!\3!\5!\u00be\n!\3\"\3\"\7\"\u00c2\n\"\f\"\16\""+
		"\u00c5\13\"\3#\6#\u00c8\n#\r#\16#\u00c9\3$\5$\u00cd\n$\3$\6$\u00d0\n$"+
		"\r$\16$\u00d1\3$\3$\7$\u00d6\n$\f$\16$\u00d9\13$\3$\3$\6$\u00dd\n$\r$"+
		"\16$\u00de\5$\u00e1\n$\3%\3%\5%\u00e5\n%\3%\3%\3&\3&\5&\u00eb\n&\3&\3"+
		"&\3\'\3\'\3\'\3\'\3(\6(\u00f4\n(\r(\16(\u00f5\3(\3(\3)\6)\u00fb\n)\r)"+
		"\16)\u00fc\3*\3*\3*\5*\u0102\n*\2\2+\3\3\5\4\7\5\t\6\13\7\r\b\17\t\21"+
		"\n\23\13\25\f\27\r\31\16\33\17\35\20\37\21!\22#\23%\24\'\25)\26+\27-\30"+
		"/\31\61\32\63\33\65\34\67\359\36;\37= ?!A\"C#E$G%I&K\'M(O)Q\2S\2\3\2\r"+
		"\6\2ffjjoouu\4\2RRrr\4\2OOoo\4\2CCcc\4\2C\\c|\7\2\60\60\62;C\\aac|\3\2"+
		"\62;\4\2$$))\5\2\13\f\17\17\"\"\7\2\f\f\17\17$$))^^\f\2$$))AA^^cdhhpp"+
		"ttvvxx\2\u0111\2\3\3\2\2\2\2\5\3\2\2\2\2\7\3\2\2\2\2\t\3\2\2\2\2\13\3"+
		"\2\2\2\2\r\3\2\2\2\2\17\3\2\2\2\2\21\3\2\2\2\2\23\3\2\2\2\2\25\3\2\2\2"+
		"\2\27\3\2\2\2\2\31\3\2\2\2\2\33\3\2\2\2\2\35\3\2\2\2\2\37\3\2\2\2\2!\3"+
		"\2\2\2\2#\3\2\2\2\2%\3\2\2\2\2\'\3\2\2\2\2)\3\2\2\2\2+\3\2\2\2\2-\3\2"+
		"\2\2\2/\3\2\2\2\2\61\3\2\2\2\2\63\3\2\2\2\2\65\3\2\2\2\2\67\3\2\2\2\2"+
		"9\3\2\2\2\2;\3\2\2\2\2=\3\2\2\2\2?\3\2\2\2\2A\3\2\2\2\2C\3\2\2\2\2E\3"+
		"\2\2\2\2G\3\2\2\2\2I\3\2\2\2\2K\3\2\2\2\2M\3\2\2\2\2O\3\2\2\2\3U\3\2\2"+
		"\2\5X\3\2\2\2\7\\\3\2\2\2\t^\3\2\2\2\13`\3\2\2\2\rc\3\2\2\2\17f\3\2\2"+
		"\2\21i\3\2\2\2\23k\3\2\2\2\25n\3\2\2\2\27w\3\2\2\2\31}\3\2\2\2\33\u0083"+
		"\3\2\2\2\35\u0085\3\2\2\2\37\u0087\3\2\2\2!\u0089\3\2\2\2#\u008b\3\2\2"+
		"\2%\u008d\3\2\2\2\'\u008f\3\2\2\2)\u0091\3\2\2\2+\u0093\3\2\2\2-\u0095"+
		"\3\2\2\2/\u0097\3\2\2\2\61\u0099\3\2\2\2\63\u009b\3\2\2\2\65\u009d\3\2"+
		"\2\2\67\u009f\3\2\2\29\u00a1\3\2\2\2;\u00a3\3\2\2\2=\u00a6\3\2\2\2?\u00b1"+
		"\3\2\2\2A\u00bd\3\2\2\2C\u00bf\3\2\2\2E\u00c7\3\2\2\2G\u00cc\3\2\2\2I"+
		"\u00e2\3\2\2\2K\u00e8\3\2\2\2M\u00ee\3\2\2\2O\u00f3\3\2\2\2Q\u00fa\3\2"+
		"\2\2S\u0101\3\2\2\2UV\7F\2\2VW\7Q\2\2W\4\3\2\2\2XY\7H\2\2YZ\7Q\2\2Z[\7"+
		"T\2\2[\6\3\2\2\2\\]\7@\2\2]\b\3\2\2\2^_\7>\2\2_\n\3\2\2\2`a\7@\2\2ab\7"+
		"?\2\2b\f\3\2\2\2cd\7>\2\2de\7?\2\2e\16\3\2\2\2fg\7?\2\2gh\7?\2\2h\20\3"+
		"\2\2\2ij\7~\2\2j\22\3\2\2\2kl\7@\2\2lm\7~\2\2m\24\3\2\2\2no\7(\2\2o\26"+
		"\3\2\2\2pq\7o\2\2qr\7g\2\2rs\7v\2\2st\7t\2\2tu\7k\2\2ux\7e\2\2vx\7o\2"+
		"\2wp\3\2\2\2wv\3\2\2\2x\30\3\2\2\2yz\7n\2\2z{\7q\2\2{~\7i\2\2|~\7n\2\2"+
		"}y\3\2\2\2}|\3\2\2\2~\32\3\2\2\2\177\u0080\7n\2\2\u0080\u0081\7q\2\2\u0081"+
		"\u0084\7i\2\2\u0082\u0084\7n\2\2\u0083\177\3\2\2\2\u0083\u0082\3\2\2\2"+
		"\u0084\34\3\2\2\2\u0085\u0086\7*\2\2\u0086\36\3\2\2\2\u0087\u0088\7+\2"+
		"\2\u0088 \3\2\2\2\u0089\u008a\7]\2\2\u008a\"\3\2\2\2\u008b\u008c\7_\2"+
		"\2\u008c$\3\2\2\2\u008d\u008e\7}\2\2\u008e&\3\2\2\2\u008f\u0090\7\177"+
		"\2\2\u0090(\3\2\2\2\u0091\u0092\7.\2\2\u0092*\3\2\2\2\u0093\u0094\7?\2"+
		"\2\u0094,\3\2\2\2\u0095\u0096\7-\2\2\u0096.\3\2\2\2\u0097\u0098\7/\2\2"+
		"\u0098\60\3\2\2\2\u0099\u009a\7,\2\2\u009a\62\3\2\2\2\u009b\u009c\7\61"+
		"\2\2\u009c\64\3\2\2\2\u009d\u009e\7\'\2\2\u009e\66\3\2\2\2\u009f\u00a0"+
		"\7<\2\2\u00a08\3\2\2\2\u00a1\u00a2\t\2\2\2\u00a2:\3\2\2\2\u00a3\u00a4"+
		"\t\3\2\2\u00a4\u00a5\t\4\2\2\u00a5<\3\2\2\2\u00a6\u00a7\t\5\2\2\u00a7"+
		"\u00a8\t\4\2\2\u00a8>\3\2\2\2\u00a9\u00aa\7v\2\2\u00aa\u00ab\7t\2\2\u00ab"+
		"\u00ac\7w\2\2\u00ac\u00b2\7g\2\2\u00ad\u00ae\7V\2\2\u00ae\u00af\7T\2\2"+
		"\u00af\u00b0\7W\2\2\u00b0\u00b2\7G\2\2\u00b1\u00a9\3\2\2\2\u00b1\u00ad"+
		"\3\2\2\2\u00b2@\3\2\2\2\u00b3\u00b4\7h\2\2\u00b4\u00b5\7c\2\2\u00b5\u00b6"+
		"\7n\2\2\u00b6\u00b7\7u\2\2\u00b7\u00be\7g\2\2\u00b8\u00b9\7H\2\2\u00b9"+
		"\u00ba\7C\2\2\u00ba\u00bb\7N\2\2\u00bb\u00bc\7U\2\2\u00bc\u00be\7G\2\2"+
		"\u00bd\u00b3\3\2\2\2\u00bd\u00b8\3\2\2\2\u00beB\3\2\2\2\u00bf\u00c3\t"+
		"\6\2\2\u00c0\u00c2\t\7\2\2\u00c1\u00c0\3\2\2\2\u00c2\u00c5\3\2\2\2\u00c3"+
		"\u00c1\3\2\2\2\u00c3\u00c4\3\2\2\2\u00c4D\3\2\2\2\u00c5\u00c3\3\2\2\2"+
		"\u00c6\u00c8\t\b\2\2\u00c7\u00c6\3\2\2\2\u00c8\u00c9\3\2\2\2\u00c9\u00c7"+
		"\3\2\2\2\u00c9\u00ca\3\2\2\2\u00caF\3\2\2\2\u00cb\u00cd\7/\2\2\u00cc\u00cb"+
		"\3\2\2\2\u00cc\u00cd\3\2\2\2\u00cd\u00e0\3\2\2\2\u00ce\u00d0\t\b\2\2\u00cf"+
		"\u00ce\3\2\2\2\u00d0\u00d1\3\2\2\2\u00d1\u00cf\3\2\2\2\u00d1\u00d2\3\2"+
		"\2\2\u00d2\u00d3\3\2\2\2\u00d3\u00d7\7\60\2\2\u00d4\u00d6\t\b\2\2\u00d5"+
		"\u00d4\3\2\2\2\u00d6\u00d9\3\2\2\2\u00d7\u00d5\3\2\2\2\u00d7\u00d8\3\2"+
		"\2\2\u00d8\u00e1\3\2\2\2\u00d9\u00d7\3\2\2\2\u00da\u00dc\7\60\2\2\u00db"+
		"\u00dd\t\b\2\2\u00dc\u00db\3\2\2\2\u00dd\u00de\3\2\2\2\u00de\u00dc\3\2"+
		"\2\2\u00de\u00df\3\2\2\2\u00df\u00e1\3\2\2\2\u00e0\u00cf\3\2\2\2\u00e0"+
		"\u00da\3\2\2\2\u00e1H\3\2\2\2\u00e2\u00e4\5%\23\2\u00e3\u00e5\5Q)\2\u00e4"+
		"\u00e3\3\2\2\2\u00e4\u00e5\3\2\2\2\u00e5\u00e6\3\2\2\2\u00e6\u00e7\5\'"+
		"\24\2\u00e7J\3\2\2\2\u00e8\u00ea\5M\'\2\u00e9\u00eb\5Q)\2\u00ea\u00e9"+
		"\3\2\2\2\u00ea\u00eb\3\2\2\2\u00eb\u00ec\3\2\2\2\u00ec\u00ed\5M\'\2\u00ed"+
		"L\3\2\2\2\u00ee\u00ef\t\t\2\2\u00ef\u00f0\3\2\2\2\u00f0\u00f1\b\'\2\2"+
		"\u00f1N\3\2\2\2\u00f2\u00f4\t\n\2\2\u00f3\u00f2\3\2\2\2\u00f4\u00f5\3"+
		"\2\2\2\u00f5\u00f3\3\2\2\2\u00f5\u00f6\3\2\2\2\u00f6\u00f7\3\2\2\2\u00f7"+
		"\u00f8\b(\3\2\u00f8P\3\2\2\2\u00f9\u00fb\5S*\2\u00fa\u00f9\3\2\2\2\u00fb"+
		"\u00fc\3\2\2\2\u00fc\u00fa\3\2\2\2\u00fc\u00fd\3\2\2\2\u00fdR\3\2\2\2"+
		"\u00fe\u0102\n\13\2\2\u00ff\u0100\7^\2\2\u0100\u0102\t\f\2\2\u0101\u00fe"+
		"\3\2\2\2\u0101\u00ff\3\2\2\2\u0102T\3\2\2\2\24\2w}\u0083\u00b1\u00bd\u00c3"+
		"\u00c9\u00cc\u00d1\u00d7\u00de\u00e0\u00e4\u00ea\u00f5\u00fc\u0101\4\2"+
		"\3\2\b\2\2";
	public static final ATN _ATN =
		new ATNDeserializer().deserialize(_serializedATN.toCharArray());
	static {
		_decisionToDFA = new DFA[_ATN.getNumberOfDecisions()];
		for (int i = 0; i < _ATN.getNumberOfDecisions(); i++) {
			_decisionToDFA[i] = new DFA(_ATN.getDecisionState(i), i);
		}
	}
}