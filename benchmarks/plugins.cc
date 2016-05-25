/*
  Copyright (C) 2011 - 2015 by the authors of the ASPECT code.

  This file is part of ASPECT.

  ASPECT is free software; you can redistribute it and/or modify
  it under the terms of the GNU General Public License as published by
  the Free Software Foundation; either version 2, or (at your option)
  any later version.

  ASPECT is distributed in the hope that it will be useful,
  but WITHOUT ANY WARRANTY; without even the implied warranty of
  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
  GNU General Public License for more details.

  You should have received a copy of the GNU General Public License
  along with ASPECT; see the file doc/COPYING.  If not see
  <http://www.gnu.org/licenses/>.
*/
#include <deal.II/grid/grid_generator.h>
#include <deal.II/grid/tria_iterator.h>
#include <deal.II/grid/tria_accessor.h>
#include <deal.II/grid/tria.h>

#include <aspect/geometry_model/box.h>
#include <aspect/postprocess/interface.h>
#include <aspect/simulator_access.h>
#include <deal.II/base/quadrature_lib.h>
#include <deal.II/fe/fe_values.h>

#include <cmath>
#include <vector>

namespace aspect
{
  namespace GeometryModel
  {
    /**
     * A class deriving from Box<dim>, which changes the upper boundary 
       with a sinusoidal perturbation of a given order and amplitude.
       The top surface is initialized with smooth sinusoidal topography.
       Subsequent refinements at the surface would do linear interpolations
       between the mesh points, potentially affecting the quality of the 
       sinusoidal perturbation. As such, if this class is used for topographic 
       relaxation benchmarks, it makes most sense to do it without mesh
       refinement.
     */
    template <int dim>
    class ReboundBox : public Box<dim>
    {
      public:
        /**
         * Generate a coarse mesh for the geometry described by this class.
         * Makes perturbs the top boundary of the box with a function
         * of the form z' = amplitude * cos(order * x )
         */
        virtual
        void create_coarse_mesh (parallel::distributed::Triangulation<dim> &coarse_grid) const;

        /**
         * Declare the parameters this class takes through input files.
         */
        static
        void
        declare_parameters (ParameterHandler &prm);

        /**
         * Read the parameters this class declares from the parameter
         * file.
         */
        virtual
        void
        parse_parameters (ParameterHandler &prm);

        /**
         * Give the depth of a point.
         */
        virtual
        double depth( const Point<dim> &position) const;

        /**
         * Give the maximal depth of a point.
         */
        virtual
        double maximal_depth() const;

      private:

        double order;  //Order of the perturbation
        double amplitude;  //amplitude of the perturbation

    };

    template <int dim>
    void
    ReboundBox<dim>::
    create_coarse_mesh (parallel::distributed::Triangulation<dim> &coarse_grid) const
    {
  
      //Call the normal Box mesh generator
      Box<dim>::create_coarse_mesh( coarse_grid );

      //move the vertices
      std::vector<bool> vertex_touched (coarse_grid.n_vertices(), false);

      typename parallel::distributed::Triangulation<dim>::active_cell_iterator cell;
      for (cell = coarse_grid.begin_active();  cell != coarse_grid.end();  ++cell)
        for(unsigned int v = 0; v < GeometryInfo<dim>::vertices_per_cell;  ++v)
          if(vertex_touched[cell->vertex_index(v)] == false)
          {
            Point<dim> &vertex = cell->vertex(v);
            vertex[dim-1] = vertex[dim-1] + std::cos(order*2.0*M_PI*vertex[0]/(this->get_extents()[0]))*
                                            amplitude*vertex[dim-1]/(this->get_extents()[dim-1]);
            vertex_touched[cell->vertex_index(v)] = true;
          }

    }

    template <int dim>
    double
    ReboundBox<dim>::maximal_depth() const
    {
      return Box<dim>::maximal_depth()+amplitude;
    }

    template <int dim>
    double
    ReboundBox<dim>::depth(const Point<dim> &position) const
    {
      return maximal_depth()-position(dim-1);
    }

    template <int dim>
    void
    ReboundBox<dim>::
    declare_parameters (ParameterHandler &prm)
    {
      Box<dim>::declare_parameters(prm);

      prm.enter_subsection("Geometry model");
      {
        prm.enter_subsection("Rebound Box");
        {
          prm.declare_entry ("Order", "1",
                             Patterns::Double (0),
                             "Order of the perturbation");
          prm.declare_entry ("Amplitude", "0.1",
                             Patterns::Double (0),
                             "Scaled amplitude of the perturbation");

        }
        prm.leave_subsection();
      }
      prm.leave_subsection();
    }



    template <int dim>
    void
    ReboundBox<dim>::parse_parameters (ParameterHandler &prm)
    {
      Box<dim>::parse_parameters(prm);

      prm.enter_subsection("Geometry model");
      {
        prm.enter_subsection("Rebound Box");
        {
          order = prm.get_double ("Order");
          amplitude = prm.get_double ("Amplitude");
        }
        prm.leave_subsection();
      }
      prm.leave_subsection();
    }

  }
}

// explicit instantiations
namespace aspect
{
  namespace GeometryModel
  {
    ASPECT_REGISTER_GEOMETRY_MODEL(ReboundBox,
                                   "rebound box",
                                   "Geometry model for benchmarking relaxation of topography.")
  }
}

namespace aspect
{
  namespace Postprocess
  {
    template <int dim>
    class InterfaceDepth : public Interface<dim>, public ::aspect::SimulatorAccess<dim>
    {
      public:
        /**
         * Evaluate the solution for interface depth.
         */
        virtual
        std::pair<std::string,std::string>
        execute (TableHandler &statistics);
    };


    template <int dim>
    std::pair<std::string,std::string>
    InterfaceDepth<dim>::execute (TableHandler &statistics)
    {
      if (this->n_compositional_fields() == 0)
        return std::pair<std::string,std::string>();

      // create a quadrature formula based on the compositional element alone.
      // be defensive about determining that a compositional field actually exists
      AssertThrow (this->introspection().base_elements.compositional_fields
                   != numbers::invalid_unsigned_int,
                   ExcMessage("This postprocessor cannot be used without compositional fields."));
      const std::vector<Point<dim> > support_points
        = this->get_fe().base_element(this->introspection().base_elements.compositional_fields).get_unit_support_points();
      const Quadrature<dim> quadrature_formula (support_points);
      const unsigned int n_q_points = quadrature_formula.size();

      FEValues<dim> fe_values (this->get_mapping(),
                               this->get_fe(),
                               quadrature_formula,
                               update_values   |
                               update_quadrature_points);

      std::vector<double> compositional_values(n_q_points);

      typename DoFHandler<dim>::active_cell_iterator
      cell = this->get_dof_handler().begin_active(),
      endc = this->get_dof_handler().end();

      std::vector<double> local_max_depth (this->n_compositional_fields(), -std::numeric_limits<double>::max());

      // compute the max depth by looping over the cells
      for (; cell!=endc; ++cell)
        if (cell->is_locally_owned())
          {
            fe_values.reinit (cell);

            for (unsigned int c=0; c<this->n_compositional_fields(); ++c)
              {
                fe_values[this->introspection().extractors.compositional_fields[c]].get_function_values (this->get_solution(),
                    compositional_values);
                for (unsigned int q=0; q<n_q_points; ++q)
                  if (compositional_values[q] > 0.5 && 
                      this->get_geometry_model().depth(fe_values.quadrature_point(q)) > local_max_depth[c])
                    local_max_depth[c] = this->get_geometry_model().depth(fe_values.quadrature_point(q));
              }
          }
      // compute the sum over all processors
      std::vector<double> global_max_depth (local_max_depth.size());
      Utilities::MPI::max (local_max_depth,
                           this->get_mpi_communicator(),
                           global_max_depth);
      // finally produce something for the statistics file
      for (unsigned int c=0; c<this->n_compositional_fields(); ++c)
        {
          statistics.add_value ("Interface depth for composition " + this->introspection().name_for_compositional_index(c),
                                global_max_depth[c]);
        }

      // also make sure that the other columns filled by the this object
      // all show up with sufficient accuracy and in scientific notation
      for (unsigned int c=0; c<this->n_compositional_fields(); ++c)
        {
          const std::string str("Interface depth for composition " + this->introspection().name_for_compositional_index(c) );
          statistics.set_precision (str, 8);
          statistics.set_scientific (str, true);
        }

      std::ostringstream output;
      output.precision(4);
      for (unsigned int c=0; c<this->n_compositional_fields(); ++c)
        output << global_max_depth[c] << '/';

      return std::pair<std::string, std::string> ("Interface depth: ",
                                                  output.str());
    }
  }
}


// explicit instantiations
namespace aspect
{
  namespace Postprocess
  {
    ASPECT_REGISTER_POSTPROCESSOR(InterfaceDepth,
                                  "interface depth",
                                  "A postprocessor that computes the maximum depth of "
                                  "a given compositional field, where maximum depth is "
                                  "given by the deepest place where C >= 0.5.")
  }
}
