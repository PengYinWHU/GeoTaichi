import sys
sys.path.append('../../..')

from geotaichi.__init__ import *
from src.__init__ import *

init(dim=2, device_memory_GB=3.7, log=False)

mpm = MPM()

mpm.set_configuration(domain=[6., 6.],
                      background_damping=0.0,
                      alphaPIC=1.0, 
                      mapping="USL", 
                      shape_function="CubicBSpline",
                      gravity=[0., -9.8],
                      material_type="Fluid",
                      velocity_projection="Taylor") #"also support for Taylor PIC"

mpm.set_solver({
                      "Timestep":         2e-6,
                      "SimulationTime":   20,
                      "SaveInterval":     5e-2,
                      "SavePath":         'NewtonianFluid2D'
                 }) 

mpm.memory_allocate(memory={
                                "max_material_number":           1,
                                "max_particle_number":           100352,
                                "verlet_distance_multiplier":    1.,
                                "max_constraint_number":  {
                                                               "max_reflection_constraint":   541681
                                                          }
                            })
                            
mpm.add_material(model="Newtonian",
                 material={
                               "MaterialID":           1,
                               "Density":              1000.,
                               "Modulus":              2e6,
                               "Viscosity":            1e-3,
                               "ElementLength":        0.02,
                               "cL":                   1.0,
                               "cQ":                   2
                 })

mpm.add_element(element={
                             "ElementType":               "Q4N2D",
                             "ElementSize":               [0.01, 0.01]
                        })


mpm.add_region(region=[{
                            "Name": "region1",
                            "Type": "Rectangle2D",
                            "BoundingBoxPoint": [0.0, 0.0],
                            "BoundingBoxSize": [2.24, 1.12],
                            "ydirection": [0., 1.]
                      }])

mpm.add_body(body={
                       "Template": [{
                                       "RegionName":         "region1",
                                       "nParticlesPerCell":  2,
                                       "BodyID":             0,
                                       "MaterialID":         1,
                                       "ParticleStress": {
                                                              "GravityField":     True,
                                                              "InternalStress":   ti.Vector([-0., -0., -0., 0., 0., 0.])
                                                         },
                                       "InitialVelocity":[0, 0, 0],
                                       "FixVelocity":    ["Free", "Free", "Free"]    
                                       
                                   }]
                   })
                   

mpm.add_boundary_condition(boundary=[
                                    {
                                        "BoundaryType":   "ReflectionConstraint",
                                        "Norm":       [-1., 0.],
                                        "StartPoint":     [0, 0],
                                        "EndPoint":       [0., 6.],
                                    },
                                    
                                    {
                                        "BoundaryType":   "ReflectionConstraint",
                                        "Norm":       [1., 0.],
                                        "StartPoint":     [6., 0],
                                        "EndPoint":       [6., 6.],
                                    },
                                    
                                    {
                                        "BoundaryType":   "ReflectionConstraint",
                                        "Norm":       [0., -1.],
                                        "StartPoint":     [0, 0],
                                        "EndPoint":       [6., 0.],
                                    },
                                    
                                    {
                                        "BoundaryType":   "ReflectionConstraint",
                                        "Norm":       [0., 1.],
                                        "StartPoint":     [0, 6.],
                                        "EndPoint":       [6., 6.],
                                    }])


mpm.select_save_data(grid=True)

mpm.run()

mpm.postprocessing(read_path='NewtonianFluid2D', write_background_grid=True)


