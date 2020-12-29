import FWCore.ParameterSet.Config as cms
from Configuration.Generator.Pythia8CommonSettings_cfi import *
from Configuration.Generator.MCTunes2017.PythiaCP5Settings_cfi import *

generator = cms.EDFilter("Pythia8GeneratorFilter",
    pythiaPylistVerbosity = cms.untracked.int32(0),
    pythiaHepMCVerbosity = cms.untracked.bool(False),
    maxEventsToPrint = cms.untracked.int32(0),
    comEnergy = cms.double(13000.0),
    ExternalDecays = cms.PSet(
        EvtGen130 = cms.untracked.PSet(
            decay_table = cms.string('GeneratorInterface/EvtGenInterface/data/DECAY_2014_NOLONGLIFE.DEC'),
            particle_property_file = cms.FileInPath('GeneratorInterface/EvtGenInterface/data/evt_2014.pdl'),
            list_forced_decays = cms.vstring('MyB+','MyB-'),
            operates_on_particles = cms.vint32(521),    # we care just about our signal particles
            convertPythiaCodes = cms.untracked.bool(False),
            user_decay_embedded= cms.vstring(
"""
#
# This is the decay file for the decay Bu -> D0munu -> K pi munu
#
Alias      MyB+   B+
Alias      MyB-   B-
ChargeConj MyB-   MyB+
Alias      MyD0   D0
Alias      Myanti-D0   anti-D0
ChargeConj MyD0   Myanti-D0
#
Decay MyB+
1.000      Myanti-D0  mu+  nu_mu            PHOTOS  ISGW2;
Enddecay
CDecay MyB-
#
#
Decay MyD0
1.000      K-  pi+                        PHSP;
Enddecay
CDecay Myanti-D0
#
End
                """
                                            )
        ),
        parameterSets = cms.vstring('EvtGen130')
    ),
    PythiaParameters = cms.PSet(
        pythia8CommonSettingsBlock,
        pythia8CP5SettingsBlock,
        processParameters = cms.vstring(
                                        # 'SoftQCD:nonDiffractive = on',
                                        'HardQCD:hardbbbar = on',
                                        'PhaseSpace:pTHatMin = 5.'
            ),
        parameterSets = cms.vstring('pythia8CommonSettings',
                                    'pythia8CP5Settings',
                                    'processParameters',
                                    )
    )
)

###### Filters ##########
bufilter = cms.EDFilter(
    "PythiaFilter",
    MaxEta = cms.untracked.double(9999999.),
    MinEta = cms.untracked.double(-9999999.),
    ParticleID = cms.untracked.int32(521) ## Bu
    )

decayfilter = cms.EDFilter(
    "PythiaDauVFilter",
    NumberDaughters = cms.untracked.int32(3),
    ParticleID      = cms.untracked.int32(521),  ## Bu
    DaughterIDs     = cms.untracked.vint32(-421, -13, 14), ## D0 mu+ nu_mu
    MinPt           = cms.untracked.vdouble(-1., -1., -1.),
    MinEta          = cms.untracked.vdouble(-9999999., -9999999., -9999999.),
    MaxEta          = cms.untracked.vdouble( 9999999.,  9999999., 9999999.)
)



d0filter = cms.EDFilter("PythiaDauVFilter",
    DaughterIDs = cms.untracked.vint32(-321, 211), # K- pi+
    MaxEta = cms.untracked.vdouble(9999999.0, 9999999.0),
    MinEta = cms.untracked.vdouble(-9999999.0, -9999999.0),
    MinPt = cms.untracked.vdouble(-1.,-1.),
    MotherID = cms.untracked.int32(-521), #Bu
    NumberDaughters = cms.untracked.int32(2),
    ParticleID = cms.untracked.int32(421), # D0
)


mufilter = cms.EDFilter("PythiaFilter",  # bachelor muon with kinematic cuts.
    MaxEta = cms.untracked.double(2.5),
    MinEta = cms.untracked.double(-2.5),
    MinPt = cms.untracked.double(4.5),
    ParticleID = cms.untracked.int32(13),
)

ProductionFilterSequence = cms.Sequence(generator + bufilter + decayfilter + d0filter + mufilter)
