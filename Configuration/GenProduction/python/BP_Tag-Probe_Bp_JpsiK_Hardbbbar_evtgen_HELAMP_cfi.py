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
            operates_on_particles = cms.vint32(521),
            convertPythiaCodes = cms.untracked.bool(False),
            user_decay_embedded= cms.vstring(
"""
#
#
#
Alias     MyJ/psi    J/psi
Decay MyJ/psi
1.000      mu+  mu-              PHOTOS   VLL;
Enddecay
#
Decay B+
1.000     MyJ/psi  K+         PHOTOS  SVS; #[Reconstructed PDG2011]
Enddecay
#
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
        processParameters = cms.vstring('HardQCD:hardbbbar = on'),
        parameterSets = cms.vstring('pythia8CommonSettings',
                                    'pythia8CP5Settings',
                                    'processParameters',
                                    )
    )
)


###### Filters ##########
mufilter = cms.EDFilter("PythiaFilter",
    MaxEta = cms.untracked.double(1.55),
    MinEta = cms.untracked.double(-1.55),
    MinPt = cms.untracked.double(6.7),
    ParticleID = cms.untracked.int32(13),
)

Bfilter = cms.EDFilter(
    "PythiaDauVFilter",
    ParticleID         = cms.untracked.int32(521),  ## B+
    ChargeConjugation  = cms.untracked.bool(False),
    NumberDaughters    = cms.untracked.int32(2),
    DaughterIDs        = cms.untracked.vint32(443, 321),
    MinPt              = cms.untracked.vdouble(-1., 0.3),
    MinEta             = cms.untracked.vdouble(-9999999., -2.5),
    MaxEta             = cms.untracked.vdouble( 9999999., 2.5)
)


JpsiFilter = cms.EDFilter(
    "PythiaDauVFilter",
    ParticleID         = cms.untracked.int32(443),  ## J/Psi
    NumberDaughters    = cms.untracked.int32(2),
    DaughterIDs        = cms.untracked.vint32(-13, 13),
    MinPt              = cms.untracked.vdouble(1., 1.),
    MinEta             = cms.untracked.vdouble(-2.5, -2.5),
    MaxEta             = cms.untracked.vdouble( 2.5, 2.5)
)


ProductionFilterSequence = cms.Sequence(generator + mufilter + Bfilter + JpsiFilter)
