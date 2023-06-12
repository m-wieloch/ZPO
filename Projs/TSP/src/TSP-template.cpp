// 8: Wieloch (303080), Rybska (401417), Sukiennik (401060)
//
// Created by Dominika on 01.11.2020.
//

#include "TSP.hpp"

#include <algorithm>
#include <stack>
#include <optional>

std::ostream& operator<<(std::ostream& os, const CostMatrix& cm) {
    for (std::size_t r = 0; r < cm.size(); ++r) {
        for (std::size_t c = 0; c < cm.size(); ++c) {
            const auto& elem = cm[r][c];
            os << (is_inf(elem) ? "INF" : std::to_string(elem)) << " ";
        }
        os << "\n";
    }
    os << std::endl;

    return os;
}

/* PART 1 */

/**
 * Create path from unsorted path and last 2x2 cost matrix.
 * @return The vector of consecutive vertex.
 */
path_t StageState::get_path() {

    path_t path_sorted;
    CostMatrix& m = const_cast<CostMatrix&>(StageState::get_matrix());

    NewVertex new_vertex = StageState::choose_new_vertex();
    StageState::append_to_path(new_vertex.coordinates);

    m[new_vertex.coordinates.row][new_vertex.coordinates.col] = INF;

    int count_inf = 0;
    for (std::size_t row = 0; row < m.size(); row++) {
        for (std::size_t col = 0; col < m.size(); col++) {
            if (m[row][col] == 0) {
                m[row][col] = INF;
                count_inf = 1;
                break;
            }
        }
        if (count_inf == 1) {
            break;
        }
    }

    cost_t lb_cost = StageState::reduce_cost_matrix();
    update_lower_bound(lb_cost);


    new_vertex = StageState::choose_new_vertex();
    StageState::append_to_path(new_vertex.coordinates);


    unsorted_path_t path_unsorted = StageState::get_unsorted_path();

    vertex_t next_vertex = path_unsorted[0];
    path_sorted.push_back(next_vertex.row);

    while (path_sorted.size() != path_unsorted.size()) {
        for (auto v : path_unsorted) {
            if (next_vertex.col == v.row) {
                next_vertex = v;
                path_sorted.push_back(next_vertex.row);
                break;
            }
        }
    }

    return path_sorted;  // DONE
}

/**
 * Get minimum values from each row and returns them.
 * @return Vector of minimum values in row.
 */
std::vector<cost_t> CostMatrix::get_min_values_in_rows() const {

    std::vector<cost_t> result;

    cost_matrix_t matrix = CostMatrix::get_matrix();

    for (std::size_t row = 0; row < matrix.size(); row++) {
        cost_t min_value_in_row = matrix[row][0];

        for (std::size_t col = 1; col < matrix.size(); col++) {
            if (matrix[row][col] < min_value_in_row)
                min_value_in_row = matrix[row][col];
        }
        result.push_back(min_value_in_row);
    }
    return result;  // DONE
}

/**
 * Reduce rows so that in each row at least one zero value is present.
 * @return Sum of values reduced in rows.
 */
cost_t CostMatrix::reduce_rows() {

    std::vector<cost_t> min_values = CostMatrix::get_min_values_in_rows();

    cost_matrix_t& m = const_cast<cost_matrix_t&>(CostMatrix::get_matrix());

    for (auto & min_value : min_values) {
        if(min_value == INF) {
            min_value = 0;
        }
    }

    for (std::size_t i = 0; i < m.size(); i++) {
        for (std::size_t j = 0; j < m.size(); j++) {
            if (is_inf(m[i][j])) continue;
            else m[i][j] = m[i][j] - min_values[i];
        }
    }

    cost_t result = std::accumulate(std::cbegin(min_values), std::cend(min_values), 0);

    return result;  // DONE
}

/**
 * Get minimum values from each column and returns them.
 * @return Vector of minimum values in columns.
 */
std::vector<cost_t> CostMatrix::get_min_values_in_cols() const {

    std::vector<cost_t> result;

    cost_matrix_t matrix = CostMatrix::get_matrix();

    for (std::size_t row = 0; row < matrix.size(); row++) {
        cost_t min_value_in_col = matrix[0][row];

        for(std::size_t col = 1; col < matrix.size(); col++){
            if (matrix[col][row] < min_value_in_col)
                min_value_in_col = matrix[col][row];
        }
        result.push_back(min_value_in_col);
    }
    return result;  // DONE
}



/**
 * Reduces rows so that in each column at least one zero value is present.
 * @return Sum of values reduced in columns.
 */
cost_t CostMatrix::reduce_cols() {
    std::vector<cost_t> min_values = CostMatrix::get_min_values_in_cols();

    cost_matrix_t& m = const_cast<cost_matrix_t&>(CostMatrix::get_matrix());

    for (auto & min_value : min_values) {
        if(min_value == INF) {
            min_value = 0;
        }
    }
    for (std::size_t i = 0; i < m.size(); i++) {
        for (std::size_t j = 0; j < m.size(); j++) {
            if (is_inf(m[j][i])) continue;
            else m[j][i] = m[j][i] - min_values[i];
        }
    }

    cost_t result = std::accumulate(std::cbegin(min_values), std::cend(min_values), 0);

    return result;  // DONE
}

/**
 * Get the cost of not visiting the vertex_t (@see: get_new_vertex())
 * @param row
 * @param col
 * @return The sum of minimal values in row and col, excluding the intersection value.
 */
cost_t CostMatrix::get_vertex_cost(std::size_t row, std::size_t col) const {

    const CostMatrix& m = CostMatrix::get_matrix();
    cost_t result = 0;
    cost_t row_min_v = 0;
    cost_t col_min_v = 0;

    if (row != 0) {
        col_min_v = m[0][col];
    }
    else {
        col_min_v = m[1][col];
    }

    for (std::size_t r = 0; r < m.size(); r++) {
        if (r != row && m[r][col] < col_min_v) {
            col_min_v = m[r][col];
        }
    }

    if (col != 0) {
        row_min_v = m[row][0];
    }
    else {
        row_min_v = m[row][1];
    }

    for (std::size_t c = 0; c < m.size(); c++) {
        if (c != col && m[row][c] < row_min_v) {
            row_min_v = m[row][c];
        }
    }

    result = col_min_v + row_min_v;

    return result;  // Done
}



/* PART 2 */

/**
 * Choose next vertex to visit:
 * - Look for vertex_t (pair row and column) with value 0 in the current cost matrix.
 * - Get the vertex_t cost (calls get_vertex_cost()).
 * - Choose the vertex_t with maximum cost and returns it.
 * @return The coordinates of the next vertex.
 */
NewVertex StageState::choose_new_vertex() {
    cost_matrix_t& m = const_cast<cost_matrix_t&>(matrix_.get_matrix());

    std::vector<std::size_t> rows;
    std::vector<std::size_t> cols;

    for (std::size_t r = 0; r < m.size(); r++){
        for (std::size_t c = 0; c < m.size(); c++){
            if (m[r][c] == 0){
                rows.push_back(r);
                cols.push_back(c);
            }
        }
    }

    std::vector<cost_t> rows_cols_cost;

    for (std::size_t i = 0; i < rows.size(); i++){
        cost_t cost = matrix_.get_vertex_cost(rows[i], cols[i]);
        rows_cols_cost.push_back(cost);
    }

    cost_t max_cost = rows_cols_cost[0];

    for (std::size_t i = 0; i < rows_cols_cost.size(); i++){
        if (rows_cols_cost[i] > max_cost){
            max_cost = rows_cols_cost[i];
        }
    }

    std::size_t index_max_cost = 0;
    for (std::size_t i = 0; i < rows_cols_cost.size(); i++){
        if (rows_cols_cost[i] == max_cost){
            index_max_cost = i;
            break;
        }
    }

    std::size_t max_val_row = rows[index_max_cost];
    std::size_t max_val_col = cols[index_max_cost];

    return NewVertex(vertex_t(max_val_row, max_val_col), max_cost); // DONE
}

/**
 * Update the cost matrix with the new vertex.
 * @param new_vertex
 */
void StageState::update_cost_matrix(vertex_t new_vertex) {

    cost_matrix_t& m = const_cast<cost_matrix_t&>(matrix_.get_matrix());
    unsorted_path_t& path_unsorted = const_cast<unsorted_path_t&>(get_unsorted_path());

    for(std::size_t r=0; r<m.size(); r++) {
        for(std::size_t c=0; c<m[r].size(); c++) {
            if(r == new_vertex.row) {
                m[r][c] = INF;
            }
            if(c == new_vertex.col) {
                m[r][c] = INF;
            }

            for(auto vertex: path_unsorted) {
                if(c == vertex.col) {
                    m[r][c] = INF;
                }
            }
        }
    }

    m[new_vertex.col][new_vertex.row] = INF;

}

/**
 * Reduce the cost matrix.
 * @return The sum of reduced values.
 */
cost_t StageState::reduce_cost_matrix() {

    cost_t sum_rows;
    sum_rows = matrix_.reduce_rows();

    cost_t sum_cols;
    sum_cols = matrix_.reduce_cols();

    cost_t result = sum_rows + sum_cols;

    return result;  // DONE
}

/**
 * Given the optimal path, return the optimal cost.
 * @param optimal_path
 * @param m
 * @return Cost of the path.
 */
cost_t get_optimal_cost(const path_t& optimal_path, const cost_matrix_t& m) {
    cost_t cost = 0;

    for (std::size_t idx = 1; idx < optimal_path.size(); ++idx) {
        cost += m[optimal_path[idx - 1]][optimal_path[idx]];
    }

    // Add the cost of returning from the last city to the initial one.
    cost += m[optimal_path[optimal_path.size() - 1]][optimal_path[0]];

    return cost;
}

/**
 * Create the right branch matrix with the chosen vertex forbidden and the new lower bound.
 * @param m
 * @param v
 * @param lb
 * @return New branch.
 */
StageState create_right_branch_matrix(cost_matrix_t m, vertex_t v, cost_t lb) {
    CostMatrix cm(m);
    cm[v.row][v.col] = INF;
    return StageState(cm, {}, lb);
}

/**
 * Retain only optimal ones (from all possible ones).
 * @param solutions
 * @return Vector of optimal solutions.
 */
tsp_solutions_t filter_solutions(tsp_solutions_t solutions) {
    cost_t optimal_cost = INF;
    for (const auto& s : solutions) {
        optimal_cost = (s.lower_bound < optimal_cost) ? s.lower_bound : optimal_cost;
    }

    tsp_solutions_t optimal_solutions;
    std::copy_if(solutions.begin(), solutions.end(),
                 std::back_inserter(optimal_solutions),
                 [&optimal_cost](const tsp_solution_t& s) { return s.lower_bound == optimal_cost; }
    );

    return optimal_solutions;
}

/**
 * Solve the TSP.
 * @param cm The cost matrix.
 * @return A list of optimal solutions.
 */
tsp_solutions_t solve_tsp(const cost_matrix_t& cm) {

    StageState left_branch(cm);

    // The branch & bound tree.
    std::stack<StageState> tree_lifo;

    // The number of levels determines the number of steps before obtaining
    // a 2x2 matrix.
    std::size_t n_levels = cm.size() - 2;

    tree_lifo.push(left_branch);   // Use the first cost matrix as the root.

    cost_t best_lb = INF;
    tsp_solutions_t solutions;

    while (!tree_lifo.empty()) {

        left_branch = tree_lifo.top();
        tree_lifo.pop();

        while (left_branch.get_level() != n_levels && left_branch.get_lower_bound() <= best_lb) {
            // Repeat until a 2x2 matrix is obtained or the lower bound is too high...

            if (left_branch.get_level() == 0) {
                left_branch.reset_lower_bound();
            }

            // 1. Reduce the matrix in rows and columns.
            cost_t new_cost = left_branch.reduce_cost_matrix(); // @TODO (KROK 1)


            // 2. Update the lower bound and check the break condition.
            left_branch.update_lower_bound(new_cost);
            if (left_branch.get_lower_bound() > best_lb) {
                break;
            }

            // 3. Get new vertex and the cost of not choosing it.
            NewVertex new_vertex = left_branch.choose_new_vertex(); // @TODO (KROK 2)

            // 4. @TODO Update the path - use append_to_path method.
            left_branch.append_to_path(new_vertex.coordinates);

            // 5. @TODO (KROK 3) Update the cost matrix of the left branch.
            left_branch.update_cost_matrix(new_vertex.coordinates);

            // 6. Update the right branch and push it to the LIFO.
            cost_t new_lower_bound = left_branch.get_lower_bound() + new_vertex.cost;
            tree_lifo.push(create_right_branch_matrix(cm, new_vertex.coordinates,
                                                      new_lower_bound));
        }

        if (left_branch.get_lower_bound() <= best_lb) {
            // If the new solution is at least as good as the previous one,
            // save its lower bound and its path.
            best_lb = left_branch.get_lower_bound();
            path_t new_path = left_branch.get_path();
            cost_t optimal_cost = get_optimal_cost(new_path, cm);
            for (std::size_t i = 0; i <= new_path.size(); i++) {
                new_path[i] = new_path[i] + 1;
            }
            solutions.push_back({optimal_cost, new_path});
        }
    }

    return filter_solutions(solutions); // Filter solutions to find only optimal ones.
}
// 8: Wieloch (303080), Rybska (401417), Sukiennik (401060)