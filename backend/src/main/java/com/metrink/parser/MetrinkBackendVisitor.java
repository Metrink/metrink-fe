// Generated from /home/wspeirs/src/metrink-fe/MetrinkBackend.g4 by ANTLR 4.7
package com.metrink.parser;
import org.antlr.v4.runtime.tree.ParseTreeVisitor;

/**
 * This interface defines a complete generic visitor for a parse tree produced
 * by {@link MetrinkBackendParser}.
 *
 * @param <T> The return type of the visit operation. Use {@link Void} for
 * operations with no return type.
 */
public interface MetrinkBackendVisitor<T> extends ParseTreeVisitor<T> {
	/**
	 * Visit a parse tree produced by {@link MetrinkBackendParser#metric_alert}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitMetric_alert(MetrinkBackendParser.Metric_alertContext ctx);
	/**
	 * Visit a parse tree produced by {@link MetrinkBackendParser#trigger_expression}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitTrigger_expression(MetrinkBackendParser.Trigger_expressionContext ctx);
	/**
	 * Visit a parse tree produced by {@link MetrinkBackendParser#comparitor}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitComparitor(MetrinkBackendParser.ComparitorContext ctx);
	/**
	 * Visit a parse tree produced by {@link MetrinkBackendParser#metric}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitMetric(MetrinkBackendParser.MetricContext ctx);
	/**
	 * Visit a parse tree produced by {@link MetrinkBackendParser#log}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitLog(MetrinkBackendParser.LogContext ctx);
	/**
	 * Visit a parse tree produced by {@link MetrinkBackendParser#event}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitEvent(MetrinkBackendParser.EventContext ctx);
	/**
	 * Visit a parse tree produced by {@link MetrinkBackendParser#field_list}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitField_list(MetrinkBackendParser.Field_listContext ctx);
	/**
	 * Visit a parse tree produced by {@link MetrinkBackendParser#field}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitField(MetrinkBackendParser.FieldContext ctx);
	/**
	 * Visit a parse tree produced by {@link MetrinkBackendParser#number_array}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitNumber_array(MetrinkBackendParser.Number_arrayContext ctx);
	/**
	 * Visit a parse tree produced by {@link MetrinkBackendParser#number_literal}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitNumber_literal(MetrinkBackendParser.Number_literalContext ctx);
	/**
	 * Visit a parse tree produced by {@link MetrinkBackendParser#relative_time_array}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitRelative_time_array(MetrinkBackendParser.Relative_time_arrayContext ctx);
	/**
	 * Visit a parse tree produced by {@link MetrinkBackendParser#relative_time_literal}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitRelative_time_literal(MetrinkBackendParser.Relative_time_literalContext ctx);
	/**
	 * Visit a parse tree produced by {@link MetrinkBackendParser#absolute_date_time_literal}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitAbsolute_date_time_literal(MetrinkBackendParser.Absolute_date_time_literalContext ctx);
	/**
	 * Visit a parse tree produced by {@link MetrinkBackendParser#absolute_date_literal}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitAbsolute_date_literal(MetrinkBackendParser.Absolute_date_literalContext ctx);
	/**
	 * Visit a parse tree produced by {@link MetrinkBackendParser#absolute_time_literal}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitAbsolute_time_literal(MetrinkBackendParser.Absolute_time_literalContext ctx);
	/**
	 * Visit a parse tree produced by {@link MetrinkBackendParser#integer_literal}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitInteger_literal(MetrinkBackendParser.Integer_literalContext ctx);
	/**
	 * Visit a parse tree produced by {@link MetrinkBackendParser#boolean_literal}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitBoolean_literal(MetrinkBackendParser.Boolean_literalContext ctx);
	/**
	 * Visit a parse tree produced by {@link MetrinkBackendParser#string_array}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitString_array(MetrinkBackendParser.String_arrayContext ctx);
	/**
	 * Visit a parse tree produced by {@link MetrinkBackendParser#regex_literal}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitRegex_literal(MetrinkBackendParser.Regex_literalContext ctx);
	/**
	 * Visit a parse tree produced by {@link MetrinkBackendParser#string_literal}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitString_literal(MetrinkBackendParser.String_literalContext ctx);
}