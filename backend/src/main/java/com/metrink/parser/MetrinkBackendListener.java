// Generated from /home/wspeirs/src/metrink-fe/MetrinkBackend.g4 by ANTLR 4.7
package com.metrink.parser;
import org.antlr.v4.runtime.tree.ParseTreeListener;

/**
 * This interface defines a complete listener for a parse tree produced by
 * {@link MetrinkBackendParser}.
 */
public interface MetrinkBackendListener extends ParseTreeListener {
	/**
	 * Enter a parse tree produced by {@link MetrinkBackendParser#metric_alert}.
	 * @param ctx the parse tree
	 */
	void enterMetric_alert(MetrinkBackendParser.Metric_alertContext ctx);
	/**
	 * Exit a parse tree produced by {@link MetrinkBackendParser#metric_alert}.
	 * @param ctx the parse tree
	 */
	void exitMetric_alert(MetrinkBackendParser.Metric_alertContext ctx);
	/**
	 * Enter a parse tree produced by {@link MetrinkBackendParser#trigger_expression}.
	 * @param ctx the parse tree
	 */
	void enterTrigger_expression(MetrinkBackendParser.Trigger_expressionContext ctx);
	/**
	 * Exit a parse tree produced by {@link MetrinkBackendParser#trigger_expression}.
	 * @param ctx the parse tree
	 */
	void exitTrigger_expression(MetrinkBackendParser.Trigger_expressionContext ctx);
	/**
	 * Enter a parse tree produced by {@link MetrinkBackendParser#comparitor}.
	 * @param ctx the parse tree
	 */
	void enterComparitor(MetrinkBackendParser.ComparitorContext ctx);
	/**
	 * Exit a parse tree produced by {@link MetrinkBackendParser#comparitor}.
	 * @param ctx the parse tree
	 */
	void exitComparitor(MetrinkBackendParser.ComparitorContext ctx);
	/**
	 * Enter a parse tree produced by {@link MetrinkBackendParser#metric}.
	 * @param ctx the parse tree
	 */
	void enterMetric(MetrinkBackendParser.MetricContext ctx);
	/**
	 * Exit a parse tree produced by {@link MetrinkBackendParser#metric}.
	 * @param ctx the parse tree
	 */
	void exitMetric(MetrinkBackendParser.MetricContext ctx);
	/**
	 * Enter a parse tree produced by {@link MetrinkBackendParser#log}.
	 * @param ctx the parse tree
	 */
	void enterLog(MetrinkBackendParser.LogContext ctx);
	/**
	 * Exit a parse tree produced by {@link MetrinkBackendParser#log}.
	 * @param ctx the parse tree
	 */
	void exitLog(MetrinkBackendParser.LogContext ctx);
	/**
	 * Enter a parse tree produced by {@link MetrinkBackendParser#event}.
	 * @param ctx the parse tree
	 */
	void enterEvent(MetrinkBackendParser.EventContext ctx);
	/**
	 * Exit a parse tree produced by {@link MetrinkBackendParser#event}.
	 * @param ctx the parse tree
	 */
	void exitEvent(MetrinkBackendParser.EventContext ctx);
	/**
	 * Enter a parse tree produced by {@link MetrinkBackendParser#field_list}.
	 * @param ctx the parse tree
	 */
	void enterField_list(MetrinkBackendParser.Field_listContext ctx);
	/**
	 * Exit a parse tree produced by {@link MetrinkBackendParser#field_list}.
	 * @param ctx the parse tree
	 */
	void exitField_list(MetrinkBackendParser.Field_listContext ctx);
	/**
	 * Enter a parse tree produced by {@link MetrinkBackendParser#field}.
	 * @param ctx the parse tree
	 */
	void enterField(MetrinkBackendParser.FieldContext ctx);
	/**
	 * Exit a parse tree produced by {@link MetrinkBackendParser#field}.
	 * @param ctx the parse tree
	 */
	void exitField(MetrinkBackendParser.FieldContext ctx);
	/**
	 * Enter a parse tree produced by {@link MetrinkBackendParser#number_array}.
	 * @param ctx the parse tree
	 */
	void enterNumber_array(MetrinkBackendParser.Number_arrayContext ctx);
	/**
	 * Exit a parse tree produced by {@link MetrinkBackendParser#number_array}.
	 * @param ctx the parse tree
	 */
	void exitNumber_array(MetrinkBackendParser.Number_arrayContext ctx);
	/**
	 * Enter a parse tree produced by {@link MetrinkBackendParser#number_literal}.
	 * @param ctx the parse tree
	 */
	void enterNumber_literal(MetrinkBackendParser.Number_literalContext ctx);
	/**
	 * Exit a parse tree produced by {@link MetrinkBackendParser#number_literal}.
	 * @param ctx the parse tree
	 */
	void exitNumber_literal(MetrinkBackendParser.Number_literalContext ctx);
	/**
	 * Enter a parse tree produced by {@link MetrinkBackendParser#relative_time_array}.
	 * @param ctx the parse tree
	 */
	void enterRelative_time_array(MetrinkBackendParser.Relative_time_arrayContext ctx);
	/**
	 * Exit a parse tree produced by {@link MetrinkBackendParser#relative_time_array}.
	 * @param ctx the parse tree
	 */
	void exitRelative_time_array(MetrinkBackendParser.Relative_time_arrayContext ctx);
	/**
	 * Enter a parse tree produced by {@link MetrinkBackendParser#relative_time_literal}.
	 * @param ctx the parse tree
	 */
	void enterRelative_time_literal(MetrinkBackendParser.Relative_time_literalContext ctx);
	/**
	 * Exit a parse tree produced by {@link MetrinkBackendParser#relative_time_literal}.
	 * @param ctx the parse tree
	 */
	void exitRelative_time_literal(MetrinkBackendParser.Relative_time_literalContext ctx);
	/**
	 * Enter a parse tree produced by {@link MetrinkBackendParser#absolute_date_time_literal}.
	 * @param ctx the parse tree
	 */
	void enterAbsolute_date_time_literal(MetrinkBackendParser.Absolute_date_time_literalContext ctx);
	/**
	 * Exit a parse tree produced by {@link MetrinkBackendParser#absolute_date_time_literal}.
	 * @param ctx the parse tree
	 */
	void exitAbsolute_date_time_literal(MetrinkBackendParser.Absolute_date_time_literalContext ctx);
	/**
	 * Enter a parse tree produced by {@link MetrinkBackendParser#absolute_date_literal}.
	 * @param ctx the parse tree
	 */
	void enterAbsolute_date_literal(MetrinkBackendParser.Absolute_date_literalContext ctx);
	/**
	 * Exit a parse tree produced by {@link MetrinkBackendParser#absolute_date_literal}.
	 * @param ctx the parse tree
	 */
	void exitAbsolute_date_literal(MetrinkBackendParser.Absolute_date_literalContext ctx);
	/**
	 * Enter a parse tree produced by {@link MetrinkBackendParser#absolute_time_literal}.
	 * @param ctx the parse tree
	 */
	void enterAbsolute_time_literal(MetrinkBackendParser.Absolute_time_literalContext ctx);
	/**
	 * Exit a parse tree produced by {@link MetrinkBackendParser#absolute_time_literal}.
	 * @param ctx the parse tree
	 */
	void exitAbsolute_time_literal(MetrinkBackendParser.Absolute_time_literalContext ctx);
	/**
	 * Enter a parse tree produced by {@link MetrinkBackendParser#integer_literal}.
	 * @param ctx the parse tree
	 */
	void enterInteger_literal(MetrinkBackendParser.Integer_literalContext ctx);
	/**
	 * Exit a parse tree produced by {@link MetrinkBackendParser#integer_literal}.
	 * @param ctx the parse tree
	 */
	void exitInteger_literal(MetrinkBackendParser.Integer_literalContext ctx);
	/**
	 * Enter a parse tree produced by {@link MetrinkBackendParser#boolean_literal}.
	 * @param ctx the parse tree
	 */
	void enterBoolean_literal(MetrinkBackendParser.Boolean_literalContext ctx);
	/**
	 * Exit a parse tree produced by {@link MetrinkBackendParser#boolean_literal}.
	 * @param ctx the parse tree
	 */
	void exitBoolean_literal(MetrinkBackendParser.Boolean_literalContext ctx);
	/**
	 * Enter a parse tree produced by {@link MetrinkBackendParser#string_array}.
	 * @param ctx the parse tree
	 */
	void enterString_array(MetrinkBackendParser.String_arrayContext ctx);
	/**
	 * Exit a parse tree produced by {@link MetrinkBackendParser#string_array}.
	 * @param ctx the parse tree
	 */
	void exitString_array(MetrinkBackendParser.String_arrayContext ctx);
	/**
	 * Enter a parse tree produced by {@link MetrinkBackendParser#regex_literal}.
	 * @param ctx the parse tree
	 */
	void enterRegex_literal(MetrinkBackendParser.Regex_literalContext ctx);
	/**
	 * Exit a parse tree produced by {@link MetrinkBackendParser#regex_literal}.
	 * @param ctx the parse tree
	 */
	void exitRegex_literal(MetrinkBackendParser.Regex_literalContext ctx);
	/**
	 * Enter a parse tree produced by {@link MetrinkBackendParser#string_literal}.
	 * @param ctx the parse tree
	 */
	void enterString_literal(MetrinkBackendParser.String_literalContext ctx);
	/**
	 * Exit a parse tree produced by {@link MetrinkBackendParser#string_literal}.
	 * @param ctx the parse tree
	 */
	void exitString_literal(MetrinkBackendParser.String_literalContext ctx);
}