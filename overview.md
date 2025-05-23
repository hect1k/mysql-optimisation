# MySQL Performance Optimization Overview

---

## 1. Indexing

### Description

Indexes are essential for accelerating query execution by allowing the database engine to quickly locate rows that satisfy filter conditions. This implementation includes:

* **Composite Indexes:** Created on multiple columns frequently combined in query `WHERE` clauses, significantly reducing the number of scanned rows.
* **Single-Column Indexes:** Added on columns with high cardinality or often used in filters and joins.
* **Functional Indexes (MySQL 8.0+):** Indexes on expressions, such as `ROUND(price, 0)`, to optimize queries using computed values.

### Impact

Indexes improve the efficiency of searches and sorts, dramatically lowering query response times for filtering and ordering operations.

### Resources

* [MySQL 8.0 Indexes Documentation](https://dev.mysql.com/doc/refman/8.0/en/mysql-indexes.html)
* [Functional Indexes in MySQL 8.0](https://dev.mysql.com/doc/refman/8.0/en/create-index.html#create-index-functional)

---

## 2. Storage Engine: InnoDB

### Description

The `InnoDB` storage engine was explicitly used for the table. `InnoDB` supports transactions, row-level locking, and robust crash recovery, making it suitable for high concurrency environments.

### Impact

* Ensures data integrity and durability.
* Improves concurrency performance by reducing lock contention.
* Provides efficient support for foreign keys and transactions.

### Resources

* [InnoDB Storage Engine](https://dev.mysql.com/doc/refman/8.0/en/innodb-storage-engine.html)
* [Choosing a Storage Engine](https://dev.mysql.com/doc/refman/8.0/en/storage-engines.html)

---

## 3. Calculated Columns as Cache

### Description

To avoid repetitive computation of frequently used derived values during query execution, a calculated column (`price_rating_cache`) was introduced. This column stores precomputed categorical labels based on the `price` (e.g., 'premium', 'midrange', 'budget').

The column is populated during data insertion and indexed to accelerate queries filtering on these categories.

### Impact

* Eliminates the overhead of computing derived values at runtime.
* Improves performance on queries filtering or grouping by these computed attributes.

### Resources

* [Generated Columns in MySQL](https://dev.mysql.com/doc/refman/8.0/en/create-table-generated-columns.html)
* [How to Use the MySQL Generated Columns](https://www.mysqltutorial.org/mysql-basics/mysql-generated-columns/)

---

## 4. Query Optimization

### Description

Several query-level optimizations were applied, including:

* **Column pruning:** Selecting only the necessary columns instead of `SELECT *`.
* **Use of indexed columns in WHERE and ORDER BY clauses:** Ensuring queries leverage indexes efficiently.
* **Rewriting subqueries as joins or derived tables:** To reduce nested query overhead.
* **Aggregation queries leveraging indexes and calculated columns:** Optimizing GROUP BY and aggregation functions.

### Impact

* Reduced CPU and IO usage per query.
* Minimized temporary table usage and filesorts.
* Improved overall query throughput.

### Resources

* [MySQL Query Optimization](https://dev.mysql.com/doc/refman/8.0/en/where-optimization.html)
* [Optimizing Queries with Indexes](https://dev.mysql.com/doc/refman/8.4/en/optimization-indexes.html)
* [EXPLAIN Statement Usage](https://dev.mysql.com/doc/refman/8.0/en/explain.html)

---

## Summary

| Optimization Strategy      | Purpose                           | Result                                  |
| -------------------------- | --------------------------------- | --------------------------------------- |
| Serious Indexing           | Speed up filters and sorts        | Dramatic query latency reduction        |
| InnoDB Storage Engine      | Reliable, concurrent transactions | Improved data integrity and concurrency |
| Calculated Columns (Cache) | Avoid runtime computation         | Faster queries on derived attributes    |
| Query Optimization         | Efficient SQL construction        | Reduced resource consumption per query  |

---

## Potential Disadvantages

While these optimizations offer significant performance improvements, there are some trade-offs to consider:

* **Increased Storage Overhead:** Indexes and calculated columns consume additional disk space, which may be considerable for very large datasets.
* **Write Performance Impact:** Maintaining multiple indexes and calculated columns can slow down `INSERT`, `UPDATE`, and `DELETE` operations due to extra index updates and cache maintenance.
* **Complexity in Maintenance:** More complex indexing and query structures can increase the difficulty of maintaining the database schema and tuning queries over time.
* **Risk of Stale Cached Data:** If calculated columns are not properly updated during data changes, cached values may become inconsistent, leading to incorrect query results.
* **Potential Over-Indexing:** Excessive indexing may lead to diminishing returns or even degrade performance, requiring careful index management and periodic review.
